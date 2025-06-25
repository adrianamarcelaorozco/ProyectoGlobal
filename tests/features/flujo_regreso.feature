Feature: Flujo de navegación con botones Regresar/Anterior

  Scenario: El usuario puede volver a la página anterior en cada paso del flujo
    Given que ingreso al sistema
    When completo los formularios iniciales
    And realizo el formulario personal y regreso
    And regreso desde el perfil financiero
    And regreso desde las metas financieras
    Then cada regreso debe llevar a la página anterior correctamente
