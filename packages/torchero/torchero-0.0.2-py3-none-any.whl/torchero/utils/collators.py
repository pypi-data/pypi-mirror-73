import torch

class PadSequenceCollate(object):
    def __init__(self, pad_sequences=True):
        self.pad_sequences = pad_sequences

    def pad_tensor(self, x, expected_size):
        assert(expected_size >= x.shape[0])
        if self.pad_sequences:
            x = torch.nn.functional.pad(x,
                                        [0] * (2 * x.dim() - 1) + [expected_size - x.shape[0]],
                                        value=-1)
        return x

    def __call__(self, batch):
        # Sort the batch in the descending order
        sorted_batch = sorted(batch, key=lambda x: x[0].shape[0], reverse=True)
        max_length = sorted_batch[0][0].shape[0]

        lengths = torch.LongTensor([x[0].shape[0] for x in sorted_batch])
        sequences = torch.stack([self.pad_tensor(x[0], expected_size=max_length)
                                     for x in sorted_batch])
        labels = torch.stack([self.pad_tensor(x[1], expected_size=max_length)
                                  for x in sorted_batch])
        #print(labels.shape)
        #print([x.shape for x in sequences])
        # Also need to store the length of each sequence
        # This is later needed in order to unpad the sequences

        # Don't forget to grab the labels of the *sorted* batch
        return (sequences, lengths), labels
