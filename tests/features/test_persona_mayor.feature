Feature: Flujo completo de cotización para una persona mayor

  Como usuario mayor de 60 años
  Quiero poder completar el flujo completo del sistema
  Para obtener una cotización válida y simular productos

  Scenario: Persona mayor puede completar todo el flujo de cotización
    Given que ingreso al sistema
    When completo el formulario inicial
    And completo el formulario personal con datos de una persona mayor
    And completo el perfil financiero
    And defino mis metas financieras
    And realizo la cotización
    Then debería poder simular diferentes productos y finalizar correctamente
