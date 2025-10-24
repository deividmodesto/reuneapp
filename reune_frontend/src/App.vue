<template>
  <div id="app-layout">
    <header>
      <nav>
        <router-link to="/">Dashboard</router-link> | 
        <router-link to="/login">Login</router-link>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
#app-layout {
  font-family: sans-serif;
}
header {
  background-color: #f8f9fa;
  padding: 1rem;
  text-align: center;
  border-bottom: 1px solid #dee2e6;
}
nav a {
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
  margin: 0 10px;
}
nav a.router-link-exact-active {
  color: #007bff;
}
main {
  padding: 2rem;
}
</style>