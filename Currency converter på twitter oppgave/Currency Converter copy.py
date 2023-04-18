from forex_python.converter import CurrencyRates
from datetime import datetime
import schedule
import tweepy

#Twitter tokens til brukeren sånt at jeg kan poste på twitter med den twitter brukeren
auth=tweepy.OAuthHandler('API-Key', 'API-Secret')
auth.set_access_token('Access-Token', 'Access-Secret')
api=tweepy.API(auth)

def job():
    #Finner ut hvor mye 1 USD er i NOK, og runder av til 5 desimaler
    currency=CurrencyRates()
    norskeKronen=round(currency.get_rate('USD', 'NOK'),5)

    #Leser øverste linje i EnUsdSist.txt filen og vi setter øverste linjen i en float variable
    read=open('EnUsdSist.txt','r')
    lines=read.readlines()
    if lines!=[]:
        førVerdi=float(lines[0])
    else:
        førVerdi=""

    if førVerdi!="":
        #Finner forskjellen mellom i dag og forrige gang vi sjekket verdien
        forskjellNOK=round(norskeKronen-førVerdi, 5)

        #Poster verdien til 1 USD i NOK og hvor mye forskjellen er
        if forskjellNOK<0:
            media=api.media_upload('img/GreenArrowDown.png')
            api.update_status(status=f'1 USD er verdt {norskeKronen} NOK. Den har gått ned med {abs(-forskjellNOK)}!', media_ids=[media.media_id])
        elif forskjellNOK>0:
            media=api.media_upload('img/RedArrowUp.png')
            api.update_status(status=f'1 USD er verdt {norskeKronen} NOK. Den har gått opp med {forskjellNOK}!', media_ids=[media.media_id])
        elif forskjellNOK==0:
            media=api.media_upload('img/GreyEqualSign.png')
            api.update_status(status=f'1 USD er verdt {norskeKronen} NOK. Den har holdt seg helt lik!', media_ids=[media.media_id])
    else:
        api.update_status(f'1 USD er verdt {norskeKronen} NOK.')

    #Åpner EnUsdSist.txt filen for å skrive inn hva verdien er i dag
    write=open('EnUsdSist.txt','w')
    write.writelines(str(norskeKronen))

    print("postet")


#Hver dag klokken 15:00 programmet gjøre funksjonen job()
schedule.every().day.at("15:00").do(job)

while True:
    #Finner hvilken dag det er 0 er mandag 6 er søndag
    x=datetime.now()
    dag=x.weekday()
    
    #Må ha "and" her fordi hvis begge er usanne så vil programmet gjøre job()
    #"or" vil gjøre job() hvis bare en av påstandene er sanne, så den ville da enda poste på lørdag og søndag
    if dag!=5 and dag!=6:
        schedule.run_pending()

#NB Forex oppdater seg bare på hverdager (mandag til fredag) og ikke i helgene, så det er derfor job() ikke skal kjøre i helgene.