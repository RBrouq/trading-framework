# Framework de Trading

## Fonctionnement

- Import de données financières via API de la part d'Alpaca(historiques et en direct) des actions US
- Formatage de cette donnée (à décider)
- Stockage dans une base de stockage(cloud, local, NAS, mixte)
- Module Core pour l'orchestration des différentes parties(et donc le lien entre les modules)
- Module Core contiendra aussi l'ensemble des classes nécessaires au fonctionnement du code
- Choix d'une stratégie
- Créer un algorithme qui permet de générer les signaux de trade basé sur la stratégie(à faire à chaque stratégie et coder de manière chronologique)
- Envoi des signaux de trading dans le stockage
- Appel des données de signaux pour réaliser le backtest
- Dans le backtest, simulation des coûts de trading et slippages
- Récupération des données de positions dans le stockage
- Appel des données de positions du backtest pour réaliser une évaluation
- Evaluation avec des métriques de permformance( globales et liée à la stratégie) et des coûts de trading
- Si le backtest est prometteur, alors on passe au paier trading
- Récupération des données live depuis données des signaux(mis continuellement à jour)
- Envoi des trades à l'API, et en,voi des logs au stockage

## Extension futures

- Passer de Alpaca à IKBR, permettant l'élargissement des classes d'actifs (et plus complet)
- Module de gestion de portefeuille afin devoir les liens entre plusieurs stratégies et actifs à la fois
- Métriques plus avancées pour l'évaluation(test statistiques, bootstrap, etc...)
- Utilisation de futures et d'options (et donc implémentation des classes associées)
- Optimisateur de stratégie basé sur du ML (position sizing, exit)
- Interface utilisateur simplifiée (Streamlit par exemple)
- Gestion des risques dynamiques