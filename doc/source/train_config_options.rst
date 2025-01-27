Configuration for training the bulkDGD model
============================================

The :meth:`core.model.BulkDGDModel.train` method requires a ``config_train`` option consisting in a dictionary with the options to train the bulkDGD model.

The dictionary should be structured as follows:

.. code-block:: python
   
   {# Set the number of epochs to train the model for.
    #
    # Type: int.
    "epochs" : 200,

    # Set the options for the data loader. They are passed to the
    # 'torch.utils.data.DataLoader' construction.
    "data_loader" : \

      {# Set how many samples per batch to load.
       #
       # Type: int.
       "batch_size" : 256,

       # Set whether to reshuffle the data during every training epoch.
       #
       # Type: bool.
       shuffle: True},

    # Set the options to output the loss.
    "loss" : \

      {# Set the options to output the GMM loss.
       "gmm" : \
         
         # Set the method used to normalize the loss when reporting it
         # per epoch.
         #
         # Type: str.
         #
         # Options:
         # - 'none' means that the loss will not be normalized.
         # - 'n_samples' means that the loss will be normalized by the
         #   number of samples.
         {"norm_method" : "n_samples"},

       # Set the options to output the reconstruction loss.
       "recon" : \
         
         # Set the method used to normalize the loss when reporting it
         # per epoch.
         #
         # Type: str.
         #
         # Options:
         # - 'none' means that the loss will not be normalized.
         # - 'n_samples' means that the loss will be normalized by the
         #   number of samples.
         {"norm_method" : "n_samples"},

       # Set the options to output the total loss.
       "total" : \

         # Set the method used to normalize the loss when reporting it
         # per epoch.
         #
         # Type: str.
         #
         # Options:
         # - 'none' means that the loss will not be normalized.
         # - 'n_samples' means that the loss will be normalized by the
         #   number of samples.
         {"norm_method" : "n_samples"}},

    # Set the options to train the Gaussian mixture model.
    "gmm" : \

        # Set the options for the optimizer.
        "optimizer" : \
        
            {# Set the name of the optimizer to be used.
             #
             # Type: str.
             #
             # Options:
             # - 'adam' for the Adam optimizer.
             "optimizer_name" : "adam",
           
             # Set the options to initialize the optimizer - they vary
             # according to the selected optimizer.
             #
             # For the 'adam' optimizer, they will be passed to the
             # 'torch.optim.Adam' constructor.
             "optimizer_options" : \

                # Set these options if 'optimizer_name' is 'adam'.

                {# Set the learning rate.
                 #
                 # Type: float.
                 "lr" : 0.01,

                 # Set the weight decay.
                 #
                 # Type: float.
                 "weight_decay" : 0.0,
                },
            },

    # Set the options to train the decoder.
    "dec" : \

        # Set the options for the optimizer.
        "optimizer" : \
        
            {# Set the name of the optimizer to be used.
             #
             # Type: str.
             #
             # Options:
             # - 'adam' for the Adam optimizer.
             "optimizer_name" : "adam",
           
             # Set the options to initialize the optimizer - they vary
             # according to the selected optimizer.
             #
             # For the 'adam' optimizer, they will be passed to the
             # 'torch.optim.Adam' constructor.
             "optimizer_options" : \

                # Set these options if 'optimizer_name' is 'adam'.

                {# Set the learning rate.
                 #
                 # Type: float.
                 "lr" : 0.0001,

                 # Set the weight decay.
                 #
                 # Type: float.
                 "weight_decay" : 0.0,

                 # Set the betas.
                 #
                 # Type: list of float.
                 "betas" : [0.5, 0.9],
                },
            },

    # Set the options to trainthe representation layer (the
    # representations found for the samples).
    "rep" : \

        # Set the options for the optimizer.
        "optimizer" : \
        
            {# Set the name of the optimizer to be used.
             #
             # Type: str.
             #
             # Options:
             # - 'adam' for the Adam optimizer.
             "optimizer_name" : "adam",
           
             # Set the options to initialize the optimizer - they vary
             # according to the selected optimizer.
             #
             # For the 'adam' optimizer, they will be passed to the
             # 'torch.optim.Adam' constructor.
             "optimizer_options" : \

                # Set these options if 'optimizer_name' is 'adam'.

                {# Set the learning rate.
                 #
                 # Type: float.
                 "lr" : 0.01,

                 # Set the weight decay.
                 #
                 # Type: float.
                 "weight_decay" : 0.0,

                 # Set the betas.
                 #
                 # Type: list of float.
                 "betas" : [0.5, 0.9],
                },
            },
    }
