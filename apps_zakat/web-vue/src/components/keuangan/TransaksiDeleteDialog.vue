<script setup lang="ts">
import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'

const props = defineProps<{
  transactionId: number
  message: string | null
  deleting: boolean
}>()

const emit = defineEmits<{
  cancel: []
  confirm: []
}>()
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
    <div class="mx-4 w-full max-w-sm rounded-xl bg-white p-6 shadow-xl">
      <h2 class="mb-2 font-semibold">Konfirmasi Hapus Transaksi</h2>
      <p class="mb-4 text-sm text-muted">
        Transaksi #{{ transactionId }} akan dihapus. Jika sudah terotorisasi, akan masuk
        antrean approval supervisor. Lanjutkan?
      </p>
      <Alert v-if="message" variant="error" :message="message" class="mb-3" />
      <div class="flex justify-end gap-3">
        <Button variant="outline" :disabled="deleting" @click="emit('cancel')">
          Batal
        </Button>
        <Button
          class="bg-red-600 text-white hover:bg-red-700"
          :disabled="deleting"
          @click="emit('confirm')"
        >
          {{ deleting ? 'Memproses...' : 'Ya, Hapus' }}
        </Button>
      </div>
    </div>
  </div>
</template>
