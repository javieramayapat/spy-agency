# Document Design for International Spy Agency 🕵️‍♂
---

## Overview: Problema a resolver

We’re building a simple tool for an international spy agency. The agency conducts
planned assassinations and has done so for decades. But it needs a new system
to assign assassinations (“hits”).

The general user is a hitman. He can be assigned a hit and see it on his list of
upcoming work. Typically, it succeeds and is closed out. But occasionally things
don’t work out and the target lives. In those cases, we assume the target hires
security and thus the case is forever closed, as a failed mission.
Like everyone else, hitmen have bosses. These are directly in charge of a group
of hitmen and can create hits and assign them. But they can only assign hits
to the hitmen they manage.

Finally, there’s the big boss of the agency - Giuseppi . He does not manage managers directly. Rather, he just has free
access to assign hits to anyone in the system. Even managers.

But when a new employee comes into the spy agency, he need not be added to The Boss’list. It’s automatic.

The boss is also in charge of assigning hitmen to managers. Only he can do that.
For simplicity, the boss is always the first user in the database.

No special indications need to be added to flag the user as the boss.

Sadly, our hitmen do occasionally die in the field. Or worse, retire from the industry.

In this case, they can no longer be assigned hits and can no longer use the system.

Managers and The Boss can however, still check old assignments for these hitmen.

### Alcance(Scope)

### Casos de uso

* Login
    * Como usuario de la agencia puedo iniciar sessión con el usuario y constraseña 💚

* Register
  * Como usuario de la plataforma me gustaria poder registrame con mi email y contraseña 💚
  * Todo usario nuevo que se registre se asigna al las lsita de hitman del big boss


* Hitman(color verde)

    -- Hits
    * Como hitman me gustaria ver mis hits asignados (filtro activos) 💚 DONE
    * Como hitman me gustaría ver el detalle de un hit 💚 DONE
    * Como hitman me gusataria marcar como Failed o Completed un hit asignado.
    * Como hitman retirado o caido en servicio no puedo volver a usar el sistema

* manager (color azul)
    * Como manager me gusatrpia poder desactivar a los hitman (solo si esta desactivado) 💚 DONE

    -- Hits
    * Como manager puedo assignar un hitman a un hit, (solo si el hitman esta a mi cargo) 💚 DONE
    * Como manager me gustaría ver todos mis hits asignados o los de mis hitman (relcion) 💚 DONE 🍎 pendiente el filtro para ver los hits de mis managers
    * Como manager me gustaría ver el detalle de un hit 💚 DONE
    * Como manger me gusatría crear hits
    * Como big boss me gustaria poder cambiar al asignado de los hits abiertos 💚 DONE

    * Como Manager si un hitman cae en una mision me gusataria marcar como Failed o Completed su hit asignado. 💚 DONE

    * * Como manager me gustaría asignar toneladas de hits. (optional ✅)


* Giuseppi (The big boss)

    -- Himen
    * Como big boss me gusatria poder ver el detalle de un hitman 💚 DONE
    * Como big boss puedo ver a todos los hitman y manager a mi cargo 💚 DONE
    * Como big boss puedo asignar hitman a un manager 💚 REPARAR VALIDACIONES
    * Como big boss me gusatrpia poder desactivar a los hitman (solo si esta desactivado) 💚 DONE
    * Como big boss si un hitman cae en una mision me gusataria marcar como Failed o Completed su hit asignado. 💚 DONE

    -- Hits
    * Como big boss puedo ver todos los hits creados 💚 DONE
    * Como big boss me gustaría ver el detalle de un hit 💚 DONE
    * Como big boss puedo asignar un user a un hit 💚 DONE
    * Como big boss me gusatria poder crear hits 💚 DONE
    * Como big boss me gusatria poder editar los hits 💚 DONE


Notas:
* El hitman al registrarse en la pagina este de inicio se asigan a la lista de elementos del big boss por defecto 💚 done
* El big boss puede asignar un hitman a un manager 💚DONE
* Si el hitma esta desactivado sus antiguas asignaciones deben poder verse en el sistema por el bog boss y el manager
* La mision puede ser cerrada tanto por el big boss y el manger del hitman ya que si una mision el objetivo muere pero el costo es el hitma esa mision se completo y se marca como tal

#### Out of Scope (casos de uso No Soportados)

* Hitman
  * Como hitman me gustaria poder asignarme mis propios hits

* Manager
  * Como hitman me gustaria poder asignarme mis propios hits
  * Como manager me gustaria poder asignarme mis propios hits
  * Como manager me gustaria poder eliminar hits
  * Cómo manager me gustaria poder asignar a más de un hitman en una hit.


##### Big Boss
* Como manager me gustaria poder asignarme mis propios hits
* Como big boss me gusatria poder eliminar hits


* Manager
  * Como Manager no puedo asignar un hit a una hitman (muerto/retirado)
  * Como manager me gustaria poder volver a activar a un hitman retirado
  * Como manager me gusatria poder asiganrle un hit a un big boss
  * Como manager no puedo asignar un hitman a otro cuyo rol no sea de manager

* Big boss
 * Como big boss puedo cambiar el rol de un hitman a un manager
 * como big boss no puedo asignar un hitman (muerto/retirado) a un manager
 * Como Big boss no puedo asignar un hit a una hitman (muerto/retirado)
 * Como Big boss me gustaria poder volver a activar a un hitman retirado
 * Como Big boss no puedo asignar un hitman a otro cuyo rol no sea de manager


Nota: Nadie puede asignar a si mismo a un hit ❌

---

## Arquitectura

### Diagramas
- API Design
- diagramas de clases
- diagramas de secuencias (no los se hacer) (evaluar si dedico tiempo a ello)

### Modelo de datos

- Diseño de entidades y atributos

- Diseño de jsons de retorno y envio de información
- Diseño de diagrama de entidad relación

#### Test cases

- Como manager no puedo asignar hits a un hitma cuyo status es retirado o caido en servicio.
- Como big boss no puedo asignar hit a un hitman cuyo status es retirado o caido en servicio
