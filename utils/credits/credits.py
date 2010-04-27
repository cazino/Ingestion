# -*- coding: utf-8 -*-

"""
Rattrapage des portefeuilles crédits
"""
from __future__ import with_statement
import os, datetime
from optparse import OptionParser

import credits_localsettings
from django.db.models import Q, Sum
from mp3.main.models import Profil, Orders, Credits, PortefeuilleCredit


def rattrape():
    # Récupère les comptes clients titulaires de crédits mondomix
    profils = Profil.objects.filter(mdx_solde__gt=0)
    for profil in profils:
        # Récupère les achats de ces crédits
        orders = Orders.validated_orders.with_currency().exclude_free_object().\
                        filter(user_id=profil.mondomix_id).order_by('validation_date').reverse()
        current_credit_solde = profil.mdx_solde
        if current_credit_solde == 0:
            break
        for order in orders:
            if current_credit_solde == 0:
                break
            panier_items = order.panier.panieritems_set.filter(object_type=4)
            for pi in panier_items:
                if current_credit_solde == 0:
                    break
                package_credit = Credits.objects.get(pk=pi.object_id)
                prix_package = getattr(package_credit.prix, "prix_%s" % order.currency.lower())
                nb_credit_to_insert = min(current_credit_solde, package_credit.nb_credit)

                # Insertion dans portefeuille crédit
                PortefeuilleCredit.objects.create(user_id=profil.mondomix_id,
                                                  nb_credit=nb_credit_to_insert,
                                                  currency=order.currency,
                                                  unit_amount=(float(prix_package)/100/package_credit.nb_credit),
                                                  exchange_rate=order.exchange_rate,
                                                  created=datetime.datetime.now(),
                                                  modified=datetime.datetime.now())
                current_credit_solde = current_credit_solde - nb_credit_to_insert
        else:
            new_credit_solde = PortefeuilleCredit.objects.\
                               filter(user_id=profil.mondomix_id).aggregate(Sum('nb_credit'))['nb_credit__sum']
            old_credit_solde = profil.mdx_solde
            try:
                assert new_credit_solde == old_credit_solde, "Pas Bon"
            except AssertionError:
                print "Old: %s  New: %s, User: %s" % (old_credit_solde, new_credit_solde, profil.mondomix_id)

def check_unbought_credit():
    profils = Profil.objects.filter(mdx_solde__gt=0)
    for profil in profils:
        # Récupère les achats de ces crédits
        orders = Orders.validated_orders.with_currency().exclude_free_object().\
                        filter(user_id=profil.mondomix_id).order_by('validation_date').reverse()
        if not orders:
            print "User: %s" % (profil.mondomix_id)
    
        
            
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--check", action="store_true", dest="check", default=False)
    parser.add_option("-r", "--rattrape", action="store_true", dest="rattrape", default=False)
    opts, args = parser.parse_args()

    if opts.check:
        check_unbought_credit()
    if opts.rattrape:
        rattrape()
