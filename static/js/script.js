const fileInput = document.getElementById('fileInput');
const optimizeBtn = document.getElementById('optimizeBtn');
const mensaje = document.getElementById('mensaje');

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    mensaje.textContent = "Imagen lista para optimizar ✨";
  };
  reader.readAsDataURL(file);
});

optimizeBtn.addEventListener('click', async () => {
  const file = fileInput.files[0];
  if (!file) {
    mensaje.textContent = "⚠️ Por favor selecciona una imagen primero.";
    return;
  }

  mensaje.textContent = "Procesando imagen con IA... ⏳";
  optimizeBtn.disabled = true;
  optimizeBtn.style.opacity = "0.6";

  const formData = new FormData();
  formData.append("imagen", file);

  try {
    const response = await fetch("/subir", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Error al comunicarse con el servidor");

    const html = await response.text();
    document.open();
    document.write(html);
    document.close();
  } catch (error) {
    mensaje.textContent = "❌ Ocurrió un error al optimizar la imagen.";
    console.error(error);
  } finally {
    optimizeBtn.disabled = false;
    optimizeBtn.style.opacity = "1";
  }
});
