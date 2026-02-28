// place files you want to import through the `$lib` alias in this folder.
export function djangoFetch(fetch: Function, cookies: any, url: string, options = {}) {
  const sessionid = cookies.get('sessionid');
  const csrftoken = cookies.get('csrftoken');
  return fetch(url, {
    ...options,
    headers: {
      'Cookie': `sessionid=${sessionid}; csrftoken=${csrftoken}`,
      ...(options as any).headers,
    }
  });
}
