from __future__ import division

from psychrnn.tasks.task import Task
import numpy as np

"""
Binary Decision task. 
Takes two channels of noisy input.
Binary output with a one hot encoding towards the higher mean channel
"""
class RDM(Task):
    def __init__(self, dt, tau, T, N_batch, coherence = None):
        super(RDM,self).__init__(2, 2, dt, tau, T, N_batch)
        self.coherence = coherence
    
    lo = 0.2
    hi = 1.0

    def generate_trial_params(self, batch, trial):

        # ----------------------------------
        # Define parameters of a trial
        # ----------------------------------
        params = dict()
        if self.coherence == None:
            params['coherence'] = np.random.choice([0.1, 0.3, 0.5, 0.7])
        else:
            params['coherence'] = self.coherence
        params['direction'] = np.random.choice([0, 1])
        params['stim_noise'] = 0.1
        params['onset_time'] = np.random.random() * self.T / 2.0
        params['stim_duration'] = np.random.random() * self.T / 4.0 + self.T / 8.0

        return params

    def trial_function(self, t, params):

        # ----------------------------------
        # Initialize with noise
        # ----------------------------------
        x_t = np.sqrt(2*self.alpha*params['stim_noise']*params['stim_noise'])*np.random.randn(self.N_in)
        y_t = np.zeros(self.N_out)
        mask_t = np.ones(self.N_out)

        # ----------------------------------
        # Retrieve parameters
        # ----------------------------------
        coh = params['coherence']
        onset = params['onset_time']
        stim_dur = params['stim_duration']
        dir = params['direction']

        # ----------------------------------
        # Compute values
        # ----------------------------------
        if onset < t < onset + stim_dur:
            x_t[dir] += 1 + coh
            x_t[(dir + 1) % 2] += 1

        if t > onset + stim_dur + 20:
            y_t[dir] = self.hi
            y_t[1-dir] = self.lo

        if t < onset + stim_dur:
            mask_t = np.zeros(self.N_out)

        return x_t, y_t, mask_t

    def accuracy_function(self, correct_output, test_output, output_mask):
        chosen = np.argmax(np.mean(test_output*output_mask, axis=1), axis = 1)
        truth = np.argmax(np.mean(correct_output*output_mask, axis = 1), axis = 1)
        return np.mean(np.equal(truth, chosen))

