<script lang="ts">
let {toggle, title = $bindable()} : {toggle(): void, title: string} = $props()
</script>

<button onclick={toggle} class="border-2 rounded-md w-2xs h-8 ">
  {title}
</button>
