<template>
    <div class="modal fade" id="modalAvatar" tabindex="-1" aria-labelledby="modalAvatarLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content bg-light text-dark rounded-4 p-3">
                <div class="modal-header border-0">
                    <h5 class="modal-title">Elegí tu avatar</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
                </div>
                <div class="modal-body d-flex flex-wrap justify-content-center gap-3">
                    <img v-for="(avatar, i) in avatars" :key="i" :src="avatar.src" class="img-avatar-modal"
                        :class="{ seleccionado: modelValue === avatar.id }" alt="avatar"
                        @click="seleccionar(avatar.id)" />


                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
  avatars: Array,
  modelValue: String
})


const emit = defineEmits(['update:modelValue'])

const seleccionar = (id) => {
  emit('update:modelValue', id)
  const modalElement = document.getElementById('modalAvatar')
  const modal = bootstrap.Modal.getInstance(modalElement)
  modal?.hide()

  // Esperamos al evento real de cierre
  modalElement.addEventListener('hidden.bs.modal', () => {
    // 🔥 Limpiar backdrop y clases que bloquean scroll/interacción
    document.body.classList.remove('modal-open')
    document.body.style.paddingRight = ''
    document.body.style.overflow = ''
    document.body.style.position = ''
    document.body.style.height = ''

    const backdrop = document.querySelector('.modal-backdrop')
    if (backdrop) backdrop.remove()
  }, { once: true })
}



</script>

<style scoped>
.img-avatar-modal {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid transparent;
    cursor: pointer;
    transition: transform 0.2s, border-color 0.2s;
}

.img-avatar-modal:hover {
    transform: scale(1.1);
    border-color: var(--colorTerciario);
}

.img-avatar-modal.seleccionado {
    border-color: var(--colorTerciario);
}
</style>
