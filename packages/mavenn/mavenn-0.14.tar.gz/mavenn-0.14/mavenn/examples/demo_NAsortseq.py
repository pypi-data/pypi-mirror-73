import mavenn
import numpy as np
from mavenn.src.utils import na_plots_for_mavenn_demo, get_example_dataset

# load data
sequences, bin_counts = get_example_dataset(name='Sort-Seq')

# load mavenn's NA model
NAR = mavenn.Model(regression_type='NA',
                   X=sequences,
                   y=bin_counts,
                   model_type='additive',
                   alphabet_dict='dna',
                   ohe_single_batch_size=50000)

NAR.fit(epochs=200,
        use_early_stopping=True,
        early_stopping_patience=20,
        verbose=1)

loss_history =  NAR.model.return_loss()

# evaluate the inferred noise model
#noise_model = NAR.na_noisemodel(sequences)
noise_model, phi_range, latent_trait = NAR.na_noisemodel(sequences, gauge_fix=True)

# plot results using helper function
na_plots_for_mavenn_demo(loss_history, NAR, noise_model, phi_range)
