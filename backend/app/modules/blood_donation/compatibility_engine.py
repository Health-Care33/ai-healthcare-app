class BloodCompatibilityEngine:

    BLOOD_COMPATIBILITY = {

        "O-": {
            "can_donate_to": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
            "can_receive_from": ["O-"]
        },

        "O+": {
            "can_donate_to": ["O+", "A+", "B+", "AB+"],
            "can_receive_from": ["O-", "O+"]
        },

        "A-": {
            "can_donate_to": ["A-", "A+", "AB-", "AB+"],
            "can_receive_from": ["O-", "A-"]
        },

        "A+": {
            "can_donate_to": ["A+", "AB+"],
            "can_receive_from": ["O-", "O+", "A-", "A+"]
        },

        "B-": {
            "can_donate_to": ["B-", "B+", "AB-", "AB+"],
            "can_receive_from": ["O-", "B-"]
        },

        "B+": {
            "can_donate_to": ["B+", "AB+"],
            "can_receive_from": ["O-", "O+", "B-", "B+"]
        },

        "AB-": {
            "can_donate_to": ["AB-", "AB+"],
            "can_receive_from": ["O-", "A-", "B-", "AB-"]
        },

        "AB+": {
            "can_donate_to": ["AB+"],
            "can_receive_from": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
        }
    }

    @classmethod
    def check_compatibility(cls, blood_group: str):

        blood_group = blood_group.upper()

        if blood_group not in cls.BLOOD_COMPATIBILITY:
            raise ValueError("Invalid Blood Group")

        compatibility = cls.BLOOD_COMPATIBILITY[blood_group]

        return {
            "blood_group": blood_group,
            "can_donate_to": compatibility["can_donate_to"],
            "can_receive_from": compatibility["can_receive_from"]
        }