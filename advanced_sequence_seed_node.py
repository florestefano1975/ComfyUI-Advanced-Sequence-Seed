# Advanced Sequence Seed Generator
# Created by AI Wiz Art (Stefano Flore)
# Version: 1.0
# https://stefanoflore.it
# https://ai-wiz.art

import random
import math
from server import PromptServer

class AdvancedSequenceSeedNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sequence_type": (["Fibonacci", "Prime", "Padovan", "Triangular", "Catalan", "Pell", "Lucas"],),
                "max_sequence_length": ("INT", {"default": 20, "min": 2, "max": 1000}),
                "seed_range_start": ("INT", {"default": 0, "min": 0, "max": 999}),
                "seed_range_end": ("INT", {"default": 19, "min": 1, "max": 1000}),
                "force_recalculation": ("BOOLEAN", {"default": True}),
                "current_seed": ("INT", {"default": 0, "min": 0, "max": 9999999999, "step": 1}),
            },
            "optional": {
                "noise_factor": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "generate_seed"
    CATEGORY = "AI WizArt"
    OUTPUT_NODE = True

    def generate_sequence(self, sequence_type, length):
        if sequence_type == "Fibonacci":
            sequence = [0, 1]
            while len(sequence) < length:
                sequence.append(sequence[-1] + sequence[-2])
        elif sequence_type == "Prime":
            sequence = self.generate_primes(length)
        elif sequence_type == "Padovan":
            sequence = [1, 1, 1]
            while len(sequence) < length:
                sequence.append(sequence[-2] + sequence[-3])
        elif sequence_type == "Triangular":
            sequence = [n * (n + 1) // 2 for n in range(1, length + 1)]
        elif sequence_type == "Catalan":
            sequence = [1]
            for n in range(1, length):
                c = sequence[-1] * 2 * (2 * n - 1) // (n + 1)
                sequence.append(c)
        elif sequence_type == "Pell":
            sequence = [0, 1]
            while len(sequence) < length:
                sequence.append(2 * sequence[-1] + sequence[-2])
        elif sequence_type == "Lucas":
            sequence = [2, 1]
            while len(sequence) < length:
                sequence.append(sequence[-1] + sequence[-2])

        return sequence

    def generate_primes(self, length):
        primes = []
        n = 2
        while len(primes) < length:
            if self.is_prime(n):
                primes.append(n)
            n += 1
        return primes

    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def generate_seed(self, sequence_type, max_sequence_length, seed_range_start, seed_range_end, force_recalculation, current_seed, noise_factor=0.0):
        if force_recalculation or current_seed == 0:
            sequence = self.generate_sequence(sequence_type, max_sequence_length)
            valid_range = sequence[seed_range_start:min(seed_range_end+1, len(sequence))]

            if not valid_range:
                raise ValueError("Invalid range specified for the sequence")

            random_index = random.randint(0, len(valid_range) - 1)
            seed = valid_range[random_index]
        else:
            seed = current_seed

        if noise_factor > 0:
            noise = random.uniform(-noise_factor, noise_factor) * seed
            seed = int(seed + noise)

        print(f"Generated seed from {sequence_type} sequence: {seed}")
        print(f"Force recalculation: {'On' if force_recalculation else 'Off'}")

        PromptServer.instance.send_sync("example.advanced_sequence_seed.update", {"seed": seed})
        return (seed,)

    @classmethod
    def IS_CHANGED(cls, force_recalculation, current_seed, **kwargs):
        if force_recalculation or current_seed == 0:
            return float("NaN")
        return ""

NODE_CLASS_MAPPINGS = {
    "AdvancedSequenceSeedNode": AdvancedSequenceSeedNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AdvancedSequenceSeedNode": "Advanced Sequence Seed Generator"
}