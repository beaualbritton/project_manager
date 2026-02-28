<script lang="ts">
  let {onSubmit = $bindable()} : {onSubmit: (username: string, password: string, event: any) => void; } = $props()

  let username: string = $state("");
  let password: string = $state("");
  let response: any = $state();

  async function handleSubmit(event: any)
  {
    event.preventDefault();

    response = onSubmit(username,password,event);
  }
</script>

<main>
  <form onsubmit={handleSubmit}>
    <div>
      <label>
        <input class="border-2" placeholder="username" bind:value={username}/>
      </label>

      <label>
        <input type="password" class="border-2" placeholder="password" bind:value={password} />
      </label>

    </div>
    <button type="submit">
      register
    </button>
  </form>
</main>
