<script setup lang="ts">
import { Banknote, Plus } from 'lucide-vue-next'
import { computed, onMounted, reactive, ref, shallowRef } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { api } from '@/lib/api/client'
import { formatDate, formatIdr } from '@/lib/format'
import { useToast } from '@/lib/useToast'

interface KasAccount {
  id: string
  code: string
  name: string
  holder: string
  balance: number
  updatedAt: string
  active: boolean
}

const accounts: KasAccount[] = [
  {
    id: 'kas-1',
    code: '1-1100',
    name: 'Kas Kecil Operasional',
    holder: 'Bendahara · Siti Aminah',
    balance: 25_000_000,
    updatedAt: '2026-05-19',
    active: true,
  },
  {
    id: 'kas-2',
    code: '1-1200',
    name: 'Kas Penyaluran Asnaf',
    holder: 'Tim Penyaluran · Ahmad Faisal',
    balance: 320_000_000,
    updatedAt: '2026-05-18',
    active: true,
  },
  {
    id: 'kas-3',
    code: '1-1300',
    name: 'Kas Booth Event Ramadhan',
    holder: 'Tim Penghimpunan · Rina Wijaya',
    balance: 12_500_000,
    updatedAt: '2026-05-19',
    active: true,
  },
  {
    id: 'kas-4',
    code: '1-1400',
    name: 'Kas Program Wakaf Produktif',
    holder: 'Tim Wakaf · Budi Setiawan',
    balance: 8_750_000,
    updatedAt: '2026-05-17',
    active: true,
  },
  {
    id: 'kas-5',
    code: '1-1500',
    name: 'Kas Cadangan Lebaran 2026',
    holder: 'Bendahara · Siti Aminah',
    balance: 0,
    updatedAt: '2026-04-30',
    active: false,
  },
]

const stats = computed(() => ({
  totalBalance: accounts.filter((a) => a.active).reduce((s, a) => s + a.balance, 0),
  totalAccounts: accounts.length,
  active: accounts.filter((a) => a.active).length,
}))


const toast = useToast()
const showAddModal = shallowRef(false)
const submitting = shallowRef(false)
const newKas = reactive({ code: '', name: '', holder: '' })

async function submitNewKas() {
  if (!newKas.code || !newKas.name) {
    toast.error('Kode dan nama kas wajib diisi')
    return
  }
  submitting.value = true
  try {
    await api.post('/api/otorisasi/submission/', {
      entity_type: 'kas',
      module: 'keuangan',
      payload: {
        code: newKas.code,
        name: newKas.name,
        holder: newKas.holder || null,
      },
    })
    toast.success('Permintaan tambah kas disubmit untuk otorisasi')
    showAddModal.value = false
    newKas.code = ''
    newKas.name = ''
    newKas.holder = ''
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal mengirim submission')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="space-y-6">
    <header class="flex flex-wrap items-start justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Manajemen Kas</h1>
        <p class="text-sm text-muted">
          Daftar brankas/kas fisik beserta saldo, pemegang, dan tanggal mutasi terakhir.
        </p>
      </div>
      <Button class="gap-1.5" @click="showAddModal = true">
        <Plus class="w-4 h-4" />
        Tambah Kas
      </Button>
    </header>

    <Alert>
      <span>
        <strong>Data dummy.</strong> Mutasi kas (input/output) akan terhubung ke modul transaksi
        keuangan di Fase 2.
      </span>
    </Alert>

    <!-- Add Kas modal -->
    <Teleport to="body">
      <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
        <div class="w-full max-w-sm rounded-xl border border-border bg-surface p-6 shadow-xl">
          <h2 class="mb-4 text-base font-semibold">Permintaan Tambah Kas</h2>
          <div class="space-y-3">
            <div>
              <label class="mb-1 block text-xs font-medium">Kode Kas <span class="text-red-500">*</span></label>
              <input
                v-model="newKas.code"
                placeholder="mis. 1-1600"
                class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
            <div>
              <label class="mb-1 block text-xs font-medium">Nama Kas <span class="text-red-500">*</span></label>
              <input
                v-model="newKas.name"
                placeholder="Nama kas / brankas"
                class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
            <div>
              <label class="mb-1 block text-xs font-medium">Pemegang Kas</label>
              <input
                v-model="newKas.holder"
                placeholder="Nama pemegang (opsional)"
                class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
          </div>
          <p class="mt-3 text-[10px] text-muted">
            Permintaan ini disubmit ke sistem otorisasi. Kas aktif setelah disetujui supervisor.
          </p>
          <div class="mt-4 flex justify-end gap-2">
            <Button variant="outline" size="sm" :disabled="submitting" @click="showAddModal = false">Batal</Button>
            <Button size="sm" :disabled="submitting" @click="submitNewKas">
              {{ submitting ? 'Mengirim...' : 'Submit Otorisasi' }}
            </Button>
          </div>
        </div>
      </div>
    </Teleport>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Total Saldo Kas</p>
          <p class="text-2xl font-bold tabular-nums text-positive">{{ formatIdr(stats.totalBalance) }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Brankas Aktif</p>
          <p class="text-2xl font-bold tabular-nums">{{ stats.active }} / {{ stats.totalAccounts }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4 flex items-center gap-3">
          <div
            class="w-10 h-10 rounded-full bg-primary/10 text-primary grid place-items-center shrink-0"
          >
            <Banknote class="w-5 h-5" />
          </div>
          <div>
            <p class="text-xs uppercase tracking-wide text-muted">Mata Uang</p>
            <p class="text-base font-semibold">Rupiah (IDR)</p>
          </div>
        </CardContent>
      </Card>
    </div>

    <Card>
      <CardContent class="p-0">
        <div class="overflow-x-auto">
          <table class="w-full text-[11px]">
            <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
              <tr class="border-b border-border">
                <th class="text-left px-4 py-2 font-medium w-24">Kode</th>
                <th class="text-left px-4 py-2 font-medium">Nama Kas</th>
                <th class="text-left px-4 py-2 font-medium max-md:hidden">Pemegang</th>
                <th class="text-right px-4 py-2 font-medium">Saldo</th>
                <th class="text-left px-4 py-2 font-medium max-md:hidden whitespace-nowrap">Update Terakhir</th>
                <th class="text-center px-4 py-2 font-medium w-20">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="a in accounts"
                :key="a.id"
                class="border-b border-border last:border-0 hover:bg-background/60"
                :class="{ 'opacity-60': !a.active }"
              >
                <td class="px-4 py-1 font-mono text-[11px] tabular-nums whitespace-nowrap">{{ a.code }}</td>
                <td class="px-4 py-1 font-medium text-[11px]">{{ a.name }}</td>
                <td class="px-4 py-1 text-muted text-[11px] max-md:hidden">{{ a.holder }}</td>
                <td class="px-4 py-1 text-right font-medium tabular-nums whitespace-nowrap">
                  {{ formatIdr(a.balance) }}
                </td>
                <td class="px-4 py-1 text-muted text-[11px] max-md:hidden whitespace-nowrap">
                  {{ formatDate(a.updatedAt) }}
                </td>
                <td class="px-4 py-1 text-center">
                  <span
                    class="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded font-medium"
                    :class="
                      a.active
                        ? 'bg-positive/15 text-positive'
                        : 'bg-background text-muted border border-border'
                    "
                  >{{ a.active ? 'Aktif' : 'Non-aktif' }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
