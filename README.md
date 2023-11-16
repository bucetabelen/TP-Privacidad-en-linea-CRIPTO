# POC Tracking Cookies
## Requisitos
- Docker
## Instrucciones
Ejecutar
```bash
docker-compose up
```  

Esto levanta 3 servidores: 
- 1 servidor de publicidades en puerto 8080  
- 2 con sitios web distintos en puertos 8081 y 8082

Sitios disponibles:
- http://localhost:8081/gatitosAdorablesPuntoCom.html
- http://localhost:8082/autosRapidosPuntoCom.html
- http://localhost:8080/history

## Uso
Navegar por `autosRapidosPuntoCom` o `gatitosAdorablesPuntoCom`.  
A medida que se "navega" por el sitio (recargar la página) la publicidad varía dependiendo del historial de navegación del usuario.  
El historial de navegación se puede ver en http://localhost:8080/history


## Ejemplo
- Navegar a http://localhost:8081/gatitosAdorablesPuntoCom.html
- La publicidad no está personalizada
- Observar abriendo las herramientas de desarrollador del navegador (F12) que se creó una cookie con el nombre `tracking-cookie` y como valor, un número (el identificador de este usuario)
- Recargar la página algunas veces, hasta que la publicidad pase a ser personalizada.
- Navegar a http://localhost:8082/autosRapidosPuntoCom.html
- Observar que se obtiene la misma cookie que en el paso 2, a pesar de estar en otra página.
- La publicidad está personalizada (con productos de gatos)
- Recargar la página algunas veces, hasta que la publicidad pase a ser de autos.
- Navegar a http://localhost:8080/history para ver todo lo que el servidor de publicidades recolectó sobre el usuario.
