<script lang="ts">
import { login } from "$lib/api/login";
import LoginForm from "$lib/components/forms/login_form.svelte";

let status: any= $state();
let message: string = $state("")


async function loginSubmit(username: string, password: string)
{
  let response = await login(username, password);
}

</script>

<main>
  <LoginForm onSubmit={loginSubmit}/>

  <h2>
    login in
  </h2>

  {#if message}
    {message}
  {:else}
    enter username and password
  {/if}

</main>
