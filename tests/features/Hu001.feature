Feature: Envío de formulario

  Scenario: Usuario envía un formulario exitosamente
    Given el usuario abre la página del formulario local
    When llena el campo "nombre" con "Adriana"
    And llena el campo "email" con "adriana@correo.com"
    And hace clic en el botón "Enviar"
    Then debería ver el mensaje "Formulario enviado con éxito"