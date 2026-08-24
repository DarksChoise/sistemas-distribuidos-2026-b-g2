# HU-[SERVICIO]-[NNN]: [Título de la Historia]

> **Convención de ID:** `HU-[SIGLA_SERVICIO]-[NNN]`
> Ejemplos: HU-IAM-001, HU-SCHED-023, HU-REF-005

---

## Historia

**Como** [rol del usuario — ej: instructor, coordinador, aprendiz, administrador]
**Quiero** [acción concreta que quiere realizar]
**Para** [beneficio que obtiene / problema que resuelve]

---

## Criterios de aceptación

> Formato: "Dado [contexto/estado inicial], cuando [acción del usuario], entonces [resultado esperado y verificable]"

- [ ] **AC1:** Dado que [contexto], cuando [acción], entonces [resultado]
- [ ] **AC2:** Dado que [contexto], cuando [acción], entonces [resultado]
- [ ] **AC3:** [Escenario de error] Dado que [contexto inválido], cuando [acción], entonces [error esperado]

---

## Notas técnicas

> [Restricciones de implementación, consideraciones de rendimiento, integraciones necesarias]

**Servicio(s) responsable(s):** [nombre del microservicio]
**Endpoint(s) que implementa:** [método + path]
**Eventos que genera:** [si aplica]
**Permisos requeridos:** [rol mínimo para ejecutar esta acción]

---

## Definición de terminado (DoD)

- [ ] Código implementado y revisado (PR aprobado por al menos 1 persona)
- [ ] Pruebas unitarias escritas (cobertura ≥ 80%)
- [ ] Pruebas de integración pasando
- [ ] Criterios de aceptación verificados manualmente o con prueba E2E
- [ ] Documentación actualizada (si aplica: contrato API, data model, runbook)
- [ ] Desplegado en ambiente de staging

---

## Estimación y prioridad

| Campo | Valor |
|-------|-------|
| Story Points | [1 / 2 / 3 / 5 / 8 / 13] |
| Prioridad | Alta / Media / Baja |
| Sprint objetivo | Sprint N |
| Dependencias | [HU-XXX-NNN que debe completarse antes] |
