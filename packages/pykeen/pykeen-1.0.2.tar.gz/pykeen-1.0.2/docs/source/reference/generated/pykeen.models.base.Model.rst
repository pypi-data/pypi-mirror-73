pykeen.models.base.Model
========================

.. currentmodule:: pykeen.models.base

.. autoclass:: Model

   
   .. automethod:: __init__

   
   .. rubric:: Methods

   .. autosummary::
   
      ~Model.__init__
      ~Model.add_module
      ~Model.apply
      ~Model.bfloat16
      ~Model.buffers
      ~Model.children
      ~Model.compute_label_loss
      ~Model.compute_mr_loss
      ~Model.compute_self_adversarial_negative_sampling_loss
      ~Model.cpu
      ~Model.cuda
      ~Model.double
      ~Model.eval
      ~Model.extra_repr
      ~Model.float
      ~Model.forward
      ~Model.get_grad_params
      ~Model.half
      ~Model.load_state
      ~Model.load_state_dict
      ~Model.modules
      ~Model.named_buffers
      ~Model.named_children
      ~Model.named_modules
      ~Model.named_parameters
      ~Model.parameters
      ~Model.post_parameter_update
      ~Model.predict_heads
      ~Model.predict_scores
      ~Model.predict_scores_all_heads
      ~Model.predict_scores_all_relations
      ~Model.predict_scores_all_tails
      ~Model.predict_tails
      ~Model.register_backward_hook
      ~Model.register_buffer
      ~Model.register_forward_hook
      ~Model.register_forward_pre_hook
      ~Model.register_parameter
      ~Model.regularize_if_necessary
      ~Model.requires_grad_
      ~Model.reset_parameters_
      ~Model.save_state
      ~Model.score_h
      ~Model.score_hrt
      ~Model.score_r
      ~Model.score_t
      ~Model.share_memory
      ~Model.state_dict
      ~Model.to
      ~Model.to_cpu_
      ~Model.to_device_
      ~Model.to_embeddingdb
      ~Model.to_gpu_
      ~Model.train
      ~Model.type
      ~Model.zero_grad
   
   

   
   
   .. rubric:: Attributes

   .. autosummary::
   
      ~Model.can_slice_h
      ~Model.can_slice_r
      ~Model.can_slice_t
      ~Model.dump_patches
      ~Model.loss_default_kwargs
      ~Model.modules_not_supporting_sub_batching
      ~Model.num_entities
      ~Model.num_parameter_bytes
      ~Model.num_relations
      ~Model.regularizer_default_kwargs
      ~Model.supports_subbatching
   
   