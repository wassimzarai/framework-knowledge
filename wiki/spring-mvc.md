---
source: raw/pdfs/9_-_Spring_MVC_-_REST.pdf
module: Architecture des SI II
tags: [spring, spring-mvc, rest, java, backend]
last_updated: 2026-06-30
---

# Spring MVC

## Overview

[[Spring]] MVC permet de créer des API web en utilisant le pattern Model-View-Controller. Spring MVC fait partie du [[Spring Framework]] et s'appuie sur la spécification JavaEE (Java Servlet). Il ne fournit pas de technologie de vue propre, mais communique avec des front-ends comme Angular ou React.

Spring MVC s'intègre aussi avec des technologies de vue serveur comme JSF, JSP, Velocity ou Thymeleaf.

## Projets Spring liés au Web

- **Spring Framework** : contient Spring MVC
- **Spring Web Flow** : navigations stateful
- **Spring Mobile** : détection du type d'appareil connecté
- **Spring Social** : intégration Facebook, Twitter, LinkedIn

## Architecture Physique (Tiers)

Voir [[Architecture des Systèmes#Tiers]] pour le détail complet. Résumé :

| Tier | Description | Exemple |
|---|---|---|
| 1-Tier | Tout sur une seule machine | Document Word local |
| 2-Tiers | Client lourd + serveur de données | Application desktop / DB server |
| 3-Tiers | Présentation / Traitement / Données séparés | App web classique (navigateur / Tomcat / DB) |
| N-Tiers | Plusieurs couches intermédiaires, microservices | GUI Angular / NodeJS / Spring Boot / MySQL |

**Inconvénient clé du 3-Tiers** : le serveur HTTP central est fortement sollicité (point de contention).

**N-Tiers en microservices** (exemple PFE Esprit "Byblos") : architecture avec `api-gateway` (Spring Cloud Zuul), `registry-server` (Eureka), `config-server`, et plusieurs microservices métier (`auth`, `PARAM`, `GED`, `fournisseur`) connectés à une base PostgreSQL commune.

## Architecture Logique (3 couches)

Une application Spring typique est structurée en trois couches logiques :

1. **Couche Présentation** : Web + Contrôleur
2. **Couche Service** : logique métier
3. **Couche Accès aux Données** : persistance des objets

Spring (via l'**IOC Container**) crée et injecte les objets nécessaires pour faire communiquer ces couches entre elles. Voir [[Spring IOC Container]].

## Serveur Web vs Serveur d'Application

| | Serveur Web | Serveur d'Application JavaEE |
|---|---|---|
| Rôle | Couche présentation uniquement, via HTTP(S) | Logique métier + présentation, multi-protocoles |
| EJB Container | Non | Oui (obligatoire) |
| Poids | Léger | Gourmand en ressources |
| Exemples | Apache HTTP Server, Tomcat, Jetty | Wildfly, WebSphere |

## Configuration de l'URL de l'application

Dans `application.properties` :
```properties
server.port=8081
server.servlet.context-path=/SpringMVC
```

## RestController — Concepts de base

```java
@RestController
public class UserRestControlImpl {
    @Autowired
    IUserService userService;

    @GetMapping("/retrieve-all-users")
    public List<User> getUsers() {
        return userService.retrieveAllUsers();
    }
}
```

`@RestController` combine `@Controller` + `@ResponseBody` : le retour de la méthode est écrit directement dans le corps de la réponse HTTP.

### Annotations HTTP principales

- `@GetMapping` → lecture
- `@PostMapping` → insertion
- `@PutMapping` → modification
- `@DeleteMapping` → suppression

### Récupération de paramètres

```java
// Variable de chemin
@GetMapping("/api/employees/{id}")
public String getEmployeeById(@PathVariable String id) { return "ID: " + id; }

// Paramètre de requête
@GetMapping("/api/foos")
public String getFoos(@RequestParam String id) { return "ID: " + id; }

// Corps de la requête désérialisé en objet Java
@PostMapping("/api/employees/add")
public Employee addEmployee(@RequestBody Employee e) { return er.save(e); }
```

## Tester avec Postman

[[Postman]] permet de construire, exécuter et historiser des requêtes HTTP pour tester les API REST (GET, POST, PUT, DELETE). Exemple observé : requête `PUT` sur `/SpringMVC/servlet/modify-client` avec un body JSON, retournant un statut `200 OK`.

## Configuration TP type (Spring Boot + Data JPA + MVC)

```properties
# Server
server.servlet.context-path=/SpringMVC
server.port=8089

# Database
spring.datasource.url=jdbc:mysql://localhost:3306/springDB?useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=

# JPA / Hibernate
spring.jpa.show-sql=true
spring.jpa.hibernate.ddl-auto=update
```

## Voir aussi

- [[Spring Boot]]
- [[Spring Data JPA]]
- [[Swagger]]
- [[Architecture des Systèmes]]
- [[Postman]]

---
*Compilé automatiquement depuis `raw/pdfs/9_-_Spring_MVC_-_REST.pdf` (cours ESPRIT, Module Architecture des SI II, 2022-2023).*
