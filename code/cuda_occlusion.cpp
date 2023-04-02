size_t numThreadsBlock = 512, currentPoints = 0;
Vertex* verticesGPU;

CUDAHandler::initializeBufferGPU(verticesGPU, batchSize);

// Initialize overlapping streams
std::vector<cudaStream_t> dataStream (numBatches);
for (auto& dataStreamId : dataStream)
{
	CUDAHandler::checkError(cudaStreamCreate(&dataStreamId));
}
 
// Execute overlapping kernels and data transfers
for (int batchId = 0; batchId < numBatches; ++batchId)
{
	size_t currentBatchSize = std::min(batchSize, pointCloudSize - currentPoints);
	CUDAHandler::checkError(cudaMemcpyAsync(&points[currentPoints], points->data(), currentBatchSize * sizeof(Vertex), cudaMemcpyHostToDevice, dataStream[batchId]));
	projectionOcclusion<<<CUDAHandler::getNumBlocks(currentBatchSize, numThreadsBlock), numThreadsBlock, 0, dataStream[batchId]>>>(verticesGPU, currentBatchSize);

	currentPoints += batchSize;
}