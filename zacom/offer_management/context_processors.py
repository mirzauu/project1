from.models import ReferralOffer,ReferralUser



def referral_offer_active(request):
    offer=ReferralOffer.objects.get(id=1)
    status = offer.is_active
    return {'referal_offer_active': status}