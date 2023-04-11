def get_inception_module(input, start_size, strides):
    conv1_a = Conv2D(start_size, (1, 1), strides=1, padding='same', activation='relu')(input)
    conv2_a = Conv2D(start_size, (3, 3), strides=strides, padding='same', activation='relu')(conv1_a)

    conv1_b = Conv2D(start_size, (1, 1), strides=1, padding='same', activation='relu')(input)
    conv2_b = Conv2D(start_size, (5, 5), strides=strides, padding='same', activation='relu')(conv1_b)

    max_pool_c = MaxPooling2D(strides, padding='same')(input)
    conv1_c = Conv2D(start_size, (1, 1), padding='same', strides=1, activation='relu')(max_pool_c)

    output = Concatenate(axis=3)([conv2_a, conv2_b, conv1_c])
    return output

in_patch = Input(shape=img_size)
x = in_patch

y = Reshape([img_size[0] * img_size[1], img_size[2]])(x)
y = Lambda(lambda z: K.l2_normalize(z, axis=-1))(y)
y = SpatialAttention()(y)
y = Reshape([img_size[0], img_size[1], img_size[2]])(y)
x = Concatenate(axis=3)([x, y])

x = Conv2D(start_size * 1, 1, strides=1, padding="same")(x)
x = Conv2D(start_size * 1, kernel_size, strides=strides, padding="same")(x)
x = LeakyReLU(alpha=0.1)(x)
x = BatchNormalization()(x)
x = Dropout(0.2)(x)
x = get_naive_inception_module(x, start_size * 2, strides=strides)
x = BatchNormalization()(x)
x = LeakyReLU(alpha=0.1)(x)
x = Dropout(0.4)(x)
x = get_inception_module(x, start_size * 6, strides=strides)
x = BatchNormalization()(x)
x = LeakyReLU(alpha=0.1)(x)
x = Flatten()(x)
x = Dropout(0.2)(x)
outputs = Dense(num_classes, activation="softmax")(x)
model = Model([in_patch], outputs)