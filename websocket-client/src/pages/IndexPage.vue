<template>
  <q-page class="flex flex-center column q-gutter-sm">
    <div>
      <q-radio v-model="status" val="hello" label="Hello" />
      <q-radio v-model="status" val="close" label="Close" />
    </div>

    <q-btn label="Send" color="primary" @click="send()" />
  </q-page>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import { Notify } from 'quasar'

const ws = new WebSocket('ws://localhost:8000')

const status = ref()

ws.onmessage = function (event) {
  console.log(event)
}

ws.onclose = function (event) {
  console.log('onclose', event)
  Notify.create('websocket connection close')
}

ws.onerror = function (error) {
  console.log('onerror', error)
}

ws.onopen = function () {
  console.log('onopen')
}

function send() {
  if (ws.readyState === 1) {
    ws.send(JSON.stringify({ status: status.value }))
  }

  else Notify.create('lost connection')
}

onUnmounted(() => {
  ws.close()
})
</script>
