## Introduction à Spring MVC
Spring MVC est un framework web basé sur le design pattern MVC (Model/View/Controller) qui permet de créer des applications web robustes et maintenables. Il fait partie du projet Spring Framework et s'intègre avec les différentes technologies de vue telles que JSF, JSP, Velocity, Thymeleaf, etc.

## Architecture Physique
Une architecture physique peut être classée en plusieurs niveaux :
- 1-Tier : tout est sur la même machine, les couches sont fortement liées
- 2-Tiers : le niveau Présentation et le niveau Traitement sont sur la machine de l'utilisateur, le niveau Base de Données est sur un autre serveur
- 3-Tiers : un niveau intermédiaire (middleware) est introduit entre le client et le serveur
- N-Tiers : assure un équilibre de charge entre le client et le serveur par l'introduction de nouvelles couches

## Architecture Logique
Une application typique utilisant Spring est généralement structurée en trois couches :
- Couche Présentation (Web + Contrôleur)
- Couche Service (interface métier)
- Couche Accès aux Données (recherche et persistance des objets)

## Serveur Web vs Serveur d'Application
Un serveur web héberge la couche Présentation et l'expose à travers le protocole HTTP(S), tandis qu'un serveur d'application héberge la logique métier et peut aussi héberger la couche Présentation.

## Spring MVC et REST
Spring MVC permet de créer des API web en utilisant le pattern Model-View-Controller. Les API REST utilisent les verbes HTTP pour effectuer des opérations CRUD. Les annotations utilisées pour les API REST sont :
- @RestController
- @GetMapping
- @PostMapping
- @PutMapping
- @DeleteMapping
- @PathVariable
- @RequestParam
- @RequestBody

## Outils de Test
Postman est un outil de test qui permet de construire et d'exécuter des requêtes HTTP. Il propose de nombreuses fonctionnalités et une interface graphique agréable.

## Exemple de Code
Un exemple de code pour un contrôleur REST :
```java
@RestController
public class UserRestControlImpl {
    @Autowired
    IUserService userService;
    
    @GetMapping("/retrieve-all-users")
    public List<User> getUsers() {
        List<User> list = userService.retrieveAllUsers(); 
        return list;
    }
}
```

## Voir aussi
- [[Spring MVC]]
- [[Postman]]
- [[JavaEE]]
- [[Spring Framework]]
- [[REST]]