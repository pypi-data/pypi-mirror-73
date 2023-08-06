pykeen.models.base.EntityEmbeddingModel
=======================================

.. currentmodule:: pykeen.models.base

.. autoclass:: EntityEmbeddingModel

   
   .. automethod:: __init__

   
   .. rubric:: Methods

   .. autosummary::
   
      ~EntityEmbeddingModel.__init__
      ~EntityEmbeddingModel.add_module
      ~EntityEmbeddingModel.apply
      ~EntityEmbeddingModel.bfloat16
      ~EntityEmbeddingModel.buffers
      ~EntityEmbeddingModel.children
      ~EntityEmbeddingModel.compute_label_loss
      ~EntityEmbeddingModel.compute_mr_loss
      ~EntityEmbeddingModel.compute_self_adversarial_negative_sampling_loss
      ~EntityEmbeddingModel.cpu
      ~EntityEmbeddingModel.cuda
      ~EntityEmbeddingModel.double
      ~EntityEmbeddingModel.eval
      ~EntityEmbeddingModel.extra_repr
      ~EntityEmbeddingModel.float
      ~EntityEmbeddingModel.forward
      ~EntityEmbeddingModel.get_grad_params
      ~EntityEmbeddingModel.half
      ~EntityEmbeddingModel.load_state
      ~EntityEmbeddingModel.load_state_dict
      ~EntityEmbeddingModel.modules
      ~EntityEmbeddingModel.named_buffers
      ~EntityEmbeddingModel.named_children
      ~EntityEmbeddingModel.named_modules
      ~EntityEmbeddingModel.named_parameters
      ~EntityEmbeddingModel.parameters
      ~EntityEmbeddingModel.post_parameter_update
      ~EntityEmbeddingModel.predict_heads
      ~EntityEmbeddingModel.predict_scores
      ~EntityEmbeddingModel.predict_scores_all_heads
      ~EntityEmbeddingModel.predict_scores_all_relations
      ~EntityEmbeddingModel.predict_scores_all_tails
      ~EntityEmbeddingModel.predict_tails
      ~EntityEmbeddingModel.register_backward_hook
      ~EntityEmbeddingModel.register_buffer
      ~EntityEmbeddingModel.register_forward_hook
      ~EntityEmbeddingModel.register_forward_pre_hook
      ~EntityEmbeddingModel.register_parameter
      ~EntityEmbeddingModel.regularize_if_necessary
      ~EntityEmbeddingModel.requires_grad_
      ~EntityEmbeddingModel.reset_parameters_
      ~EntityEmbeddingModel.save_state
      ~EntityEmbeddingModel.score_h
      ~EntityEmbeddingModel.score_hrt
      ~EntityEmbeddingModel.score_r
      ~EntityEmbeddingModel.score_t
      ~EntityEmbeddingModel.share_memory
      ~EntityEmbeddingModel.state_dict
      ~EntityEmbeddingModel.to
      ~EntityEmbeddingModel.to_cpu_
      ~EntityEmbeddingModel.to_device_
      ~EntityEmbeddingModel.to_embeddingdb
      ~EntityEmbeddingModel.to_gpu_
      ~EntityEmbeddingModel.train
      ~EntityEmbeddingModel.type
      ~EntityEmbeddingModel.zero_grad
   
   

   
   
   .. rubric:: Attributes

   .. autosummary::
   
      ~EntityEmbeddingModel.can_slice_h
      ~EntityEmbeddingModel.can_slice_r
      ~EntityEmbeddingModel.can_slice_t
      ~EntityEmbeddingModel.dump_patches
      ~EntityEmbeddingModel.loss_default_kwargs
      ~EntityEmbeddingModel.modules_not_supporting_sub_batching
      ~EntityEmbeddingModel.num_entities
      ~EntityEmbeddingModel.num_parameter_bytes
      ~EntityEmbeddingModel.num_relations
      ~EntityEmbeddingModel.regularizer_default_kwargs
      ~EntityEmbeddingModel.supports_subbatching
   
   