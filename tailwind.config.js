/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './example_django/templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
