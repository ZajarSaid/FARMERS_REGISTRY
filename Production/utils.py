
# output_verification instance creation 
from User.models import OutputVerification, Farmer

class OutputVerificationUtil:

    @staticmethod
    def create_output_verification(owner, farm_name, farm_output, status='pending'):
        verification_message = f"Your farm has been filled with an output of {farm_output}. Click VERIFY to accept or DENY to ignore."
        pending_message = "Your farm has been denied by you as an unacceptable output. Verify again or contact admin buttons."
        
        output_verification = OutputVerification.objects.create(
            owner=owner,
            farm_name=farm_name,
            farm_output=farm_output,
            verification_message=verification_message,
            pending_message=pending_message,
            status=status
        )
        
        return output_verification