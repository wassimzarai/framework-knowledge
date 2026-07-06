# SKILL: scaffolding-microapp

## Entrées attendues
- Nom de la micro-app (ex: "user-service")
- Port à utiliser (ex: 8081)

## Outils à utiliser
- Spring Initializr (start.spring.io)
- Maven

## Résultat attendu
- Un dossier avec :
  - `pom.xml` configuré (Spring Boot, Java 17+)
  - Structure MVC standard (`controller/`, `service/`, `repository/`, `model/`)
  - Un endpoint `/health` fonctionnel qui retourne `200 OK`
  - Fichier `application.properties` avec le port configuré

## Procédure
1. Générer le projet via Spring Initializr avec les dépendances : Spring Web, Spring Boot DevTools
2. Créer la structure de dossiers MVC
3. Ajouter un `HealthController` avec un endpoint GET `/health`
4. Configurer le port dans `application.properties`
5. Vérifier que le projet démarre sans erreur