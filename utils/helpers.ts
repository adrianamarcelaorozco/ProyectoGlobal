export function generarIdentificacionAleatoria(): string {
  // Generate a random identification number
  return Math.floor(Math.random() * 9000000000) + 1000000000 + '';
}

// Lists of names and surnames
const nombres = ["María", "Ana", "Laura", "Sofía", "Adriana", "Camila", "Catalina", "Dayan", "Paula", "Consuelo"];
const apellidos = ["Gómez", "Pérez", "Rodríguez", "López", "Martínez", "Fernández", "García", "Ramírez", "Torres", "Castro"];

export function generarIdentificacionAleatoria8(): string {
  // Generate a random 8-digit identification number
  return Math.floor(Math.random() * 90000000) + 10000000 + '';
}

export function generarNumeroTelefono(): string {
  return Math.floor(Math.random() * 100000000) + 600000000 + '';
}

export function generarCorreoAleatorio(): string {
  const dominios = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"];
  const caracteres = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let nombre = '';
  for (let i = 0; i < 8; i++) {
    nombre += caracteres.charAt(Math.floor(Math.random() * caracteres.length));
  }
  const dominio = dominios[Math.floor(Math.random() * dominios.length)];
  return `${nombre}@${dominio}`;
}

export function generarNombreCompleto(): [string, string, string] {
  // Generate a complete name with first name, first surname and second surname separately
  const nombre = nombres[Math.floor(Math.random() * nombres.length)];
  const apellido1 = apellidos[Math.floor(Math.random() * apellidos.length)];
  const apellido2 = apellidos[Math.floor(Math.random() * apellidos.length)];
  return [nombre, apellido1, apellido2];
}

