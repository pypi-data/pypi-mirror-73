pykeen.models.base.MultimodalModel
==================================

.. currentmodule:: pykeen.models.base

.. autoclass:: MultimodalModel

   
   .. automethod:: __init__

   
   .. rubric:: Methods

   .. autosummary::
   
      ~MultimodalModel.__init__
      ~MultimodalModel.add_module
      ~MultimodalModel.apply
      ~MultimodalModel.bfloat16
      ~MultimodalModel.buffers
      ~MultimodalModel.children
      ~MultimodalModel.compute_label_loss
      ~MultimodalModel.compute_mr_loss
      ~MultimodalModel.compute_self_adversarial_negative_sampling_loss
      ~MultimodalModel.cpu
      ~MultimodalModel.cuda
      ~MultimodalModel.double
      ~MultimodalModel.eval
      ~MultimodalModel.extra_repr
      ~MultimodalModel.float
      ~MultimodalModel.forward
      ~MultimodalModel.get_grad_params
      ~MultimodalModel.half
      ~MultimodalModel.load_state
      ~MultimodalModel.load_state_dict
      ~MultimodalModel.modules
      ~MultimodalModel.named_buffers
      ~MultimodalModel.named_children
      ~MultimodalModel.named_modules
      ~MultimodalModel.named_parameters
      ~MultimodalModel.parameters
      ~MultimodalModel.post_parameter_update
      ~MultimodalModel.predict_heads
      ~MultimodalModel.predict_scores
      ~MultimodalModel.predict_scores_all_heads
      ~MultimodalModel.predict_scores_all_relations
      ~MultimodalModel.predict_scores_all_tails
      ~MultimodalModel.predict_tails
      ~MultimodalModel.register_backward_hook
      ~MultimodalModel.register_buffer
      ~MultimodalModel.register_forward_hook
      ~MultimodalModel.register_forward_pre_hook
      ~MultimodalModel.register_parameter
      ~MultimodalModel.regularize_if_necessary
      ~MultimodalModel.requires_grad_
      ~MultimodalModel.reset_parameters_
      ~MultimodalModel.save_state
      ~MultimodalModel.score_h
      ~MultimodalModel.score_hrt
      ~MultimodalModel.score_r
      ~MultimodalModel.score_t
      ~MultimodalModel.share_memory
      ~MultimodalModel.state_dict
      ~MultimodalModel.to
      ~MultimodalModel.to_cpu_
      ~MultimodalModel.to_device_
      ~MultimodalModel.to_embeddingdb
      ~MultimodalModel.to_gpu_
      ~MultimodalModel.train
      ~MultimodalModel.type
      ~MultimodalModel.zero_grad
   
   

   
   
   .. rubric:: Attributes

   .. autosummary::
   
      ~MultimodalModel.can_slice_h
      ~MultimodalModel.can_slice_r
      ~MultimodalModel.can_slice_t
      ~MultimodalModel.dump_patches
      ~MultimodalModel.loss_default_kwargs
      ~MultimodalModel.modules_not_supporting_sub_batching
      ~MultimodalModel.num_entities
      ~MultimodalModel.num_parameter_bytes
      ~MultimodalModel.num_relations
      ~MultimodalModel.regularizer_default_kwargs
      ~MultimodalModel.supports_subbatching
   
   