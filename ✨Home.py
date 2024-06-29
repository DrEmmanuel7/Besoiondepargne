import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Simulation du besoin d'épargne",
    page_icon=":sparkles:",
    layout="wide",

)



   

hide_footer = """
<style>
#MainMenu {visibility: hidden; }
footer {visibility: hidden;}
</style>
"""
#st.markdown(hide_footer, unsafe_allow_html=True)

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col2.title(" :sparkles: Home")


#st.title("Simulation de Pension de Retraite")

# Navigation entre les pages
#page = st.sidebar.selectbox("Navigation", ["Accueil", "Informations Personnelles", "Résultats"])


st.header("Bienvenue à l'application de Simulation du besoin d'épargne")
st.write("""
        Cette application est conçue pour vous aider à évaluer le montant d'épargne dont vous aurez besoin pour maintenir 
        votre niveau de vie à la retraite. Nous allons calculer votre pension et estimer vos dépenses à la retraite afin de 
        déterminer s'il existe un écart entre vos revenus et vos besoins.
        """)

st.write("""
        En utilisant cette application, vous pourrez :
        - Estimer votre pension de retraite en fonction de votre âge, sexe, revenu et statut professionnel.
        - Évaluer vos dépenses mensuelles à la retraite en tenant compte de votre situation familiale et des besoins de vos enfants.
        - Identifier l'écart entre votre pension estimée et vos dépenses projetées.
        - Obtenir des recommandations sur le montant à épargner pour combler cet écart.
        """)

# Fonction pour calculer la pension de base pour CNPS ou salarié
def calcul_pension_cnps(revenu, age_retraite, annee_naissance):
    taux_rendement = 0.015
    duree_carriere = age_retraite - (age - annee_naissance)
    salaire_moyen = revenu
    pension_base = taux_rendement * duree_carriere * salaire_moyen
    return pension_base

# Fonction pour calculer la pension de base pour CGRAE ou fonctionnaire
def calcul_pension_cgrae(age_retraite, annee_naissance):
    NAL = age_retraite - (age - annee_naissance)
    TAL = 0.0175
    I = 2445
    V = 2801.48
    pension_base = NAL * TAL * I * V
    return pension_base





st.header("Veuillez remplir les champs suivants")

c1, c2, c3 = st.columns(3)
age = c1.number_input("Âge", min_value=15, max_value=100, value=30, step=1)
age_retraite = c1.number_input("Âge à la Retraite", min_value=50, max_value=100, value=65, step=1)
regime_retraite = c1.selectbox("Régime de Retraite", ["CNPS", "CGRAE"])
regime = regime_retraite
sexe = c2.selectbox("Sexe", ["Homme", "Femme"])
revenu = c2.number_input("Revenu Annuel", min_value=0, value=50000, step=1000)
complementaire = c2.selectbox("Avez-vous une complémentaire à la pension de base ?", ["Non", "Oui"])

annee_naissance = c3.number_input("nombre d'année de service", min_value=1, max_value=55, value=3, step=1)
statut = c3.selectbox("Statut Professionnel", ["Fonctionnaire", "Salarié"])
    
    

montant_complementaire = 0
if complementaire == "Oui":
    montant_complementaire = st.c2.number_input("Montant de la complémentaire", min_value=0, value=0, step=100)


st.header("Informations pour Estimer les Dépenses")
    
c1, c2, c3 = st.columns(3)
depense_mensuelle = c1.number_input("Dépense Moyenne Mensuelle Totale individuelle", min_value=0, value=2000, step=100)
nombre_enfants = c2.number_input("Nombre d'Enfants", min_value=0, value=0, step=1)
situation_maritale = c3.selectbox("Situation Maritale", ["Marié(e)", "Non Marié(e)"])
conjoint_travail = False
if situation_maritale == "Marié(e)":
        conjoint_travail = st.checkbox("Est-ce que votre conjoint travaille ?")
    
        

st.header("Résultats de la Simulation")
    
    # Calcul de la pension de base
    #m = regime_retraite
if regime == "CNPS" or statut == "Salarié":
        pension_base = calcul_pension_cnps(revenu, age_retraite, annee_naissance)
else:
        pension_base = calcul_pension_cgrae(age_retraite, annee_naissance)
        
    # Calcul de la pension totale
pension_totale = pension_base + montant_complementaire
    
    # Calcul du taux de remplacement
liste = []
for i in range(1, (age_retraite - (age - annee_naissance)+1)):
    revenui = revenu*(1+0.02)**(i)
    liste.append(revenui)
    
revenu_15_derniere_annee = sum(liste[-15:])/len(liste[-15:])
st.write(revenu_15_derniere_annee)
taux_remplacement = round((pension_totale/revenu_15_derniere_annee),2)
    
    # Calcul des dépenses totales mensuelles à la retraite
depense_annuelle_retraite = depense_mensuelle * 4.4 * 12 * (1 + 0.02) ** (age_retraite - (age - annee_naissance))
depense_totale_mensuelle = depense_annuelle_retraite / 12
    
    # Affichage des résultats
c1,c3 = st.columns(2)

c1.metric("Pension Totale:", round(pension_totale,0))
c1.metric("Taux de Remplacement:", taux_remplacement)
c1.metric("Dépense Totale Mensuelle à la Retraite:", round(depense_totale_mensuelle, 0))
with c3:
      
        cat = ["revenu", "depense"]
        value = [pension_totale, depense_totale_mensuelle ]
        fig, ax = plt.subplots(figsize=(3,1))
        bars = ax.bar(cat, value, color=["red","green"])
        ax.set_xlabel(" ")
        ax.set_ylabel("montants")
        ax.set_title("Revenu et depense à la retraite")
        st.pyplot(fig)
    # Calcul de l'écart pension-dépense
ecart = round(abs(pension_totale - depense_totale_mensuelle),0)
if pension_totale < depense_totale_mensuelle:
        c1, c2,c3 = st.columns(3)
        
        c2.subheader("Besoin d'épargne")
        st.warning(f"A la retraite, votre Pension sera inférieure aux dépenses de {ecart} FCFA")
        st.info(f"pour assurer un équilibre entre depense et pension il faire fait un investissement pouvant rapporter {ecart} FCFA de plus")

        c1, c2 = st.columns((3, 8))
        
         # Sélection du taux d'intérêt
        taux_interet = c1.selectbox("Taux d'Intérêt:", ["2.0%", "2.5%", "3.0%", "3.5%", "4.0%", "4.5%", "5.0%", "5.5%", "6.0%"], index=0)
        
       
    # Calcul du montant à épargner par an pour combler l'écart
        n = age_retraite - (age - annee_naissance)
        A = ecart * (1 + (float(taux_interet.strip("%"))/100)) ** (-n)
        c2.metric("Montant à Épargner par An (A):", round(A, 0))

    # Graphiques
        
        #st.bar_chart({"Revenu": [revenu / 12], "nouvelle Pension Totale": [pension_totale]})
        #c2.bar_chart(cat, value,x_label=["pension totale","depenses totales mensuelle"])     
        
else:
        st.success(f"Pension supérieure aux dépenses de {ecart}")
    
st.write("Écart (P):", ecart)
    
   
