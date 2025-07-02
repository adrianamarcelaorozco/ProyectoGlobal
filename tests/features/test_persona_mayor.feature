Feature: Flujo completo de cotización para una persona mayor

  Scenario: Persona mayor puede completar todo el flujo de cotización
    Given que ingreso al sistema
    When completo los formularios iniciales como persona mayor
    And realizo el formulario como persona mayor y continuo
    And completo el perfil financiero como persona mayor y continuo
    And defino mis metas financieras como persona mayor y continuo
    And realizo la cotización
    Then debería poder simular diferentes productos y finalizar correctamente
