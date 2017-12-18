import logging

import numpy as np


class SkipGram:
    """ Simple skip gram iterator. The negative samples are sampled uniformly from the input
    sequence.
    """

    def __init__(self):
        pass

    @staticmethod
    def iterator(sequence, window_size, negative_samples):
        """ An iterator which at each step returns a tuple of (word, context, label) """
        for i in range(len(sequence)):
            window_start = max(0, i - window_size)
            window_end = min(len(sequence), i + window_size + 1)
            for j in range(window_start, window_end):
                if i != j:
                    yield (sequence[i], sequence[j], 1)

            for negative in range(negative_samples):
                j = np.random.randint(0, len(sequence))
                yield (sequence[i], sequence[j], 0)

    @staticmethod
    def batch_iterator(sequence, window_size, negative_samples, batch_size):
        """ An iterator which returns training instances in batches """
        iterator = SkipGram.iterator(sequence, window_size, negative_samples)
        epoch = 0
        while True:
            words = np.empty(shape=batch_size, dtype=int)
            contexts = np.empty(shape=batch_size, dtype=int)
            labels = np.empty(shape=batch_size, dtype=int)
            for i in range(batch_size):
                try:
                    word, context, label = next(iterator)
                except StopIteration:
                    epoch += 1
                    logging.info("iterated %d times over data set", epoch)
                    iterator = SkipGram.iterator(sequence, window_size, negative_samples)
                    word, context, label = next(iterator)
                words[i] = word
                contexts[i] = context
                labels[i] = label
            yield ([words, contexts], labels)
