# Informes de Gestión Humana CHVS

Informes gerenciales mensuales del **separador de expedientes** (repo privado
`erpplaneacion-eng/gestion_humana_documentos`). Se publican con GitHub Pages
para compartirlos en las reuniones:

- Portada: https://erpplaneacion-eng.github.io/informes-chvs/
- Octubre 2026: https://erpplaneacion-eng.github.io/informes-chvs/2026-10/

> **Este repositorio es PÚBLICO.** Cualquiera con el enlace ve lo que hay
> aquí. Nunca debe entrar una cédula, un nombre, una foto de expediente ni
> una clave (Ley 1581 de 2012). Las páginas llevan `noindex` y `robots.txt`
> bloquea buscadores, pero eso no las hace privadas.

## Sesión de Claude Code donde se hizo

El informe de octubre se construyó en esta sesión. Para retomarla con todo
el contexto (decisiones, correcciones, mediciones), abrir una terminal en la
carpeta del repo de la app y ejecutar:

```bash
cd C:\Users\User\OneDrive\Desktop\CHVS\gestion_humana_documentos
claude --resume 4e26fd50-acd4-42ce-9734-851f1f505183
```

Solo funciona en el equipo donde se hizo (la sesión vive en
`~/.claude/projects/`). En otro equipo, este README es la guía.

## Estructura

```
index.html                 portada: un enlace por informe
2026-10/index.html         informe de octubre (autocontenido: CSS, JS y logo dentro)
marca/isotipo.png          las manos, recortadas de la pág. 5 del manual de marca
herramientas/              scripts para sacar las cifras y armar el HTML
robots.txt, .nojekyll
```

## Cómo hacer el informe del mes siguiente

1. **Copiar el anterior**: `2026-10/` → `2026-11/` y editar ahí. El HTML es
   autocontenido; la maqueta 3D usa three.js r128 desde cdnjs.
2. **Sacar las cifras reales** del volumen de Railway (ver abajo). No poner
   números de memoria: en octubre se colaron dos cifras viejas (30 min de
   proceso y "lote más grande 2.341 hojas") que la medición desmintió.
3. **Avances**: `git log --since=<inicio> --format="%ad %s" --date=short` en
   el repo de la app, y traducirlos a lo que cambia para el usuario, sin
   jerga técnica. Agrupar por etapas.
4. **Comprobar el estado de lo que se diga "en uso"**: qué imagen corre en
   RunPod (`list-endpoints` → campo `image`) y si incluye el commit. En
   octubre el clasificador nuevo salió como "pendiente" y ya estaba desplegado.
5. **Auditar** antes de subir:
   ```bash
   sed 's|data:image/png;base64,[A-Za-z0-9+/=]*||' 2026-11/index.html \
     | grep -nE '[0-9]{7,}|sk-[A-Za-z0-9]+'      # no debe salir nada
   ```
6. Añadir la línea del mes en `index.html`, commit y push a `main`. Pages
   publica solo en ~1 minuto.

Si el informe se trabaja primero como Artifact de Claude (sin `<!doctype>`
ni `<head>`), `herramientas/envolver_artifact.py entrada.html salida.html`
lo convierte en página independiente.

## De dónde salen las cifras

Todas se leen del volumen `/datos/trabajos` del servicio
`gestion_humana_documentos` en Railway (proyecto **Tecnico**). Se ejecutan
con `railway ssh` desde la carpeta del repo de la app:

```bash
B64=$(base64 -w0 herramientas/volumen.py)
railway ssh "echo $B64 | base64 -d > /tmp/v.py && python3 /tmp/v.py"
```

| Cifra | Script / comando | Qué cuenta |
|---|---|---|
| Hojas, lotes, GB | `volumen.py` | `n_paginas` y `tam_mb` del `estado.json` de cada lote padre |
| Contrataciones | `volumen.py` | carpetas `corte_*` dentro de `salida/<persona>/` |
| Documentos | `volumen.py` | PDF dentro de `corte_*/documentos/` |
| Acciones de revisión | `volumen.py` | líneas de `revision.jsonl` |
| Tiempo por lote | `tiempos.py` | `max(fin) - min(inicio)` de las partes de cada lote |
| Documentos por tipo | ver abajo | nombre del PDF sin el rango de páginas |

```bash
railway ssh "cd /datos/trabajos && find . -path '*documentos/*.pdf' | sed -E 's|.*/||; s|\.pdf$||; s|^([0-9]+_)?p[0-9]+-p[0-9]+_||' | sort | uniq -c | sort -rn | head -25"
```

Comprobar también que ningún lote esté dos veces (mismo `archivo` y
`n_paginas`), o las cifras salen infladas.

Las cifras de **calidad** (98,7 %, 94,5 %, 89 → 97 %, 86 → 109 de 120) no
salen del volumen: son mediciones contra marcas hechas a mano, documentadas
en la memoria del proyecto y en los commits del clasificador.

**Cifras de octubre (13-oct-2026):** 50.606 hojas, 33 lotes, 13,6 GB,
1.064 contrataciones, 21.335 documentos, 3.262 acciones de revisión; un lote
de ~2.500 hojas tarda ~10 min (el de 6.616, 15 min).

## Estilo: manual de marca CHVS 2026

Fuente: `OneDrive\Desktop\CHVS\manual_marca_CHVS_2026-v1.pdf`.

- Colores: negro; verde oscuro Pantone 355 `#00923F`; verde claro Pantone
  360 `#76B82A`; barra inferior `#76B82A` | `#268C39`; palabra de fondo `#F1F8F3`.
- Letras: League Spartan (títulos), Poppins (textos), Baskerville itálica
  solo para "Corporación Hacia un Valle Solidario" (en web, Libre Baskerville).
- Elementos: palabra gigante en verde pálido detrás de cada título, títulos
  en degradado claro→oscuro con corazón, tarjetas `#F7F7F7` redondeadas,
  barra de dos verdes al pie. Tema claro siempre, como el manual.
- Excepción deliberada: en la maqueta la **cédula va en amarillo** (`#E8A317`);
  en verde se confundía con los documentos y se perdía la idea del corte.

## Lo que pidió quien presenta (para no repetir errores)

- Lenguaje para gerencia: "contratación" en vez de "vinculación", "documento
  separado" en vez de "documento individual". Cifras reales, nunca ejemplos.
- La maqueta 3D: vista alejada (se ve toda la banda), sin recorrido
  automático, Anterior/Siguiente pequeños; la idea de la cédula como
  separador va dentro de la animación, no aparte.
- Sin sección de pendientes y riesgos ni glosario.
- El periodo cubre desde el inicio del proyecto (26-ago-2026) si no hubo
  informe anterior; si lo hubo, empezar donde terminó ese.
