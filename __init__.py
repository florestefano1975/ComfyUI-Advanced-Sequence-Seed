from .advanced_sequence_seed_node import AdvancedSequenceSeedNode

NODE_CLASS_MAPPINGS = {
    "AdvancedSequenceSeedNode": AdvancedSequenceSeedNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AdvancedSequenceSeedNode": "Advanced Sequence Seed Generator"
}

WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']