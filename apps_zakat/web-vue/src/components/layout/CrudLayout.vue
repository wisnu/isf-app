<template>
  <div class="space-y-3">
    <slot name="header" />
    <slot name="alert" />
    <div class="grid grid-cols-1 lg:grid-cols-[256px_1fr] gap-3 items-start">
      <slot name="filter" />
      <slot name="data" />
    </div>
  </div>
</template>
