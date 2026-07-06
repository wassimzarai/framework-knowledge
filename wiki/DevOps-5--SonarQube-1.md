## Introduction
SonarQube est un outil de test statique, open-source, qui analyse le code source pour détecter et corriger les problèmes de qualité, tels que les bugs, les vulnérabilités de sécurité et les mauvaises pratiques de codage. Il permet de mesurer la qualité du code source en continu (revue de code automatique).

## Caractéristiques de SonarQube
Les principales fonctionnalités de SonarQube sont :
* Analyse du code source
* Prise en charge de nombreux langages (Java, .Net (C#), Python, PHP, JavaScript, …)
* Détection de problèmes dans le code, comme les bugs et les vulnérabilités
* Mesure de la qualité du code avec des métriques
* Intégration avec des outils de gestion de projets et de développement
* Création de rapports détaillés sur la qualité du code et son évolution
* Personnalisation des règles de qualité
* Support de l'intégration continue (CI/CD)

## Installation de SonarQube
L'installation de SonarQube peut être effectuée à partir d'une image Docker. Les étapes sont les suivantes :
1. Télécharger l'image Docker de SonarQube
2. Exécuter le conteneur SonarQube
3. Accéder à l'interface web de SonarQube

## Utilisation de SonarQube
SonarQube peut être utilisé pour analyser la qualité du code d'un projet. Les étapes sont les suivantes :
1. Accéder à l'interface web de SonarQube
2. Créer un projet et télécharger le code source
3. Exécuter l'analyse du code
4. Consulter les résultats de l'analyse

## Intégration avec Jenkins
SonarQube peut être intégré avec Jenkins pour automatiser l'analyse de la qualité du code. Les étapes sont les suivantes :
1. Accéder à Jenkins et créer un nouveau stage
2. Exécuter les commandes Maven pour récupérer le code source et le compiler
3. Exécuter la commande Maven sonar:sonar pour analyser la qualité du code
4. Consulter les résultats de l'analyse sur l'interface web de SonarQube

## Analyse des résultats
Les résultats de l'analyse de SonarQube incluent :
* Les bugs et les vulnérabilités détectées
* Les zones à vérifier (Hotspots Reviewed)
* Le pourcentage de duplications de code
* Le taux de couverture (Coverage)
* Les mauvaises pratiques de codage (Code Smells)

## Voir aussi
* [[9---Spring-MVC---REST]]
* [[spring-mvc]]
* [[Jenkins]]
* [[Maven]]
* [[Java]]
* [[DevOps]]