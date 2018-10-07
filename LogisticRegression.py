#
# Project 1, starter code part a
#
import math
import tensorflow as tf
import numpy as np
import pylab as plt


# scale data
def scale(X, X_min, X_max):
	# Normalization 
    return (X - X_min)/(X_max-X_min)




NUM_FEATURES = 36
NUM_CLASSES = 6 # Classes are 1,2,3,4,5,7 ; 6 has been excluded from the dataset due to invalidity of the class

learning_rate = 0.01
epochs = 1000
batch_size = 4
num_neurons = 10
seed = 10
beta = 10e-6 # Regularization parameter
np.random.seed(seed)

# Creating a 3 layer neural network
def ffn(x, hidden_units):
    # Hidden layer
    with tf.name_scope('hidden'):
        weight_1 = tf.Variable(tf.truncated_normal([NUM_FEATURES, hidden_units], stddev=1.0/math.sqrt(float(NUM_FEATURES))), name='weights')
        biases = tf.Variable(tf.zeros([hidden_units]), name='biases')
        hidden = tf.nn.relu(tf.matmul(x, weight_1) + biases)


    with tf.name_scope('softmax_linear'):
        weight_2 = tf.Variable(tf.truncated_normal([hidden_units, NUM_CLASSES], stddev=1.0/math.sqrt(float(NUM_FEATURES))), name='weights')
        biases  = tf.Variable(tf.zeros([NUM_CLASSES]), name='biases')
        logits  = tf.matmul(hidden, weight_2) + biases
        
    return logits, weight_1, weight_2


#read train data
train_input = np.loadtxt('sat_train.txt',delimiter=' ')
trainX, train_Y = train_input[:,:36], train_input[:,-1].astype(int) # train_input[:,-1] starts from last input basically labels
trainX = scale(trainX, np.min(trainX, axis=0), np.max(trainX, axis=0)) # axis 0 = rows
train_Y[train_Y == 7] = 6 # Convert those of class 7 to class 6

trainY = np.zeros((train_Y.shape[0], NUM_CLASSES)) # Creates empty predicted values
trainY[np.arange(train_Y.shape[0]), train_Y-1] = 1 # One hot matrix


# experiment with small datasets
trainX = trainX[:1000]
trainY = trainY[:1000]

# shape refers to a tuple (row, columns)
n = trainX.shape[0] # 0 refers to number of rows

test_input = np.loadtxt('sat_test.txt', delimiter=' ')
testX, test_Y = test_input[:,:36], test_input[:,-1].astype(int)
testX = scale(testX, np.min(testX, axis=0), np.max(testX, axis=0))
test_Y[test_Y == 7] = 6

testY = np.zeros((test_Y.shape[0], NUM_CLASSES))
testY[np.arange(test_Y.shape[0]), test_Y-1] = 1


# Create the model
x = tf.placeholder(tf.float32, [None, NUM_FEATURES])
y_ = tf.placeholder(tf.float32, [None, NUM_CLASSES])

# Build the graph for the deep net
predicted, w1, w2 = ffn(x, num_neurons)

cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_, logits=predicted)
# Loss function using L2 regularization
regularizer = tf.nn.l2_loss(w1) + tf.nn.l2_loss(w2)
loss = tf.reduce_mean(cross_entropy + beta * regularizer)

# Create the gradient descent optimizer with the given learning rate.
optimizer = tf.train.GradientDescentOptimizer(learning_rate)
train_op = optimizer.minimize(loss)

correct_prediction = tf.cast(tf.equal(tf.argmax(predicted, axis=1), tf.argmax(y_, axis=1)), tf.float32) # Cast to float
accuracy = tf.reduce_mean(correct_prediction)

N = len(trainX)
idx = (np.arange(N))

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    train_error = []
    test_acc = []
    for i in range(epochs):
        np.random.shuffle(idx) # Shuffles the index of the dataset
        trainX = trainX[idx]
        trainY = trainY[idx]
        for start, end in zip(range(0, N, batch_size), range(batch_size, N, batch_size)): # Creates a list of ranges
            train_op.run(feed_dict={x: trainX[start:end], y_: trainY[start:end]})

        # Training Error and Accuracies
        train_error.append(loss.eval(feed_dict={x: trainX, y_: trainY}))    
        test_acc.append(accuracy.eval(feed_dict={x:testX, y_: testY}))

        # train_acc.append(accuracy.eval(feed_dict={x: trainX, y_: trainY}))

        if i % 100 == 0:
            print('The total model accuracy on the test data at epoch {} is {}'.format(i,test_acc[i])) # Testing acc
        #     print('iter %d: accuracy %g'%(i, train_acc[i])) # Training acc
            # print('iter %d: test accuracy %g'%(i, test_acc[i])) # Testing acc

        

# plot learning curves
plt.figure(1)
plt.plot(range(epochs), test_acc)
plt.xlabel(str(epochs) + ' iterations')
plt.ylabel('Test accuracy')
plt.show()

plt.figure(2)
plt.plot(range(epochs), train_error)
plt.xlabel(str(epochs) + 'iterations')
plt.ylabel('Training Error')
plt.show()
