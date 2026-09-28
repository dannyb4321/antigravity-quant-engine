# Política de Seguridad

## Versiones Soportadas

Actualmente, solo la rama principal (`main`) cuenta con soporte y actualizaciones de seguridad continuas.

| Versión | Soportada |
| ------- | --------- |
| main / 1.0.x | :white_check_mark: |
| < 1.0.0 | :x: |

## Reporte de Vulnerabilidades y Buenas Prácticas

Este motor cuantitativo interactúa con APIs financieras y maneja variables sensibles de entorno.

### Cómo reportar un fallo de seguridad
Si identificás una vulnerabilidad de seguridad o una potencial exposición de datos:
1. **No abras un Issue público** para evitar exponer vectores de ataque.
2. Enviá un reporte detallado vía email a: `dannyb@outlook.com.ar`.
3. El reporte será revisado dentro de las 48 horas hábiles para evaluar el impacto y aplicar el parche correspondiente.

### Manejo de Credenciales
- Este proyecto utiliza variables de entorno mediante archivos `.env` (excluidos explícitamente en `.gitignore`).
- Nunca ingreses tus claves de API o credenciales en texto plano dentro de ningún archivo commiteado.
