# What
A Svelte Timeline component.
This is what is looks like:
![image info](https://github.com/SumitBando/svelte-timeline/raw/main/static/timeline-sample.png "Sample")

If time permits, will try to remove dependencies.

Original Tailwind snippet was from: https://codepen.io/sheikh_ishaan/pen/oNWpgoK

# Use
## Install
```bash
npm i svelte-timeline
```

To use, pass an array of Event objects, which has at least a title.
```code
/**
 * @typedef {Object} Event
 * @property {string} title
 * @property {string} [date]
 * @property {string} [status]
 */
 ```

A date field, if passed, is shown.
Though it is used to display a sequence of timed events, the component has no understanding of time, you can pass arbitary string in the date field, or even omit it.

The 'status' field controls the color and associated icon displayed for an Event.
If the value is 'success', it is displayed a background of bg-green-500, with a fa-check-circle icon.

For 'error', it is displayed with a background of bg-red-500, with a fa-times-circle icon.

If a status field is not included, it is displayed with a background of bg-gray-300, with text color of text-gray-400, with a fa-exclamation-circle icon.

The above values are all props, and can be overridden.

If the optional prop 'heading' is passed, it is displayed at top.

In your route or component,
```
<script>
 import {Timeline} from 'svelte-timeline'
 const events = [
  {
   title: 'Step1',
   date: 'Dec 18, 2021',
   status: 'success'      
  },
  {
   title: 'Step2',
   status: 'error'
  },
  {
   title: 'Step3',
  }
 ]  
<script>

<Timeline {events} heading='Something'/>
```

## Developing

To improve this, fork this project.

After you have installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev
# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building npm package

```bash
npx svelte-kit package
```

## To test locally without publishing
```bash
npx svelte-kit package
cd package
npm link
```
Cd to a test project
```bash
npm link svelte-timeline
```


## Random notes
This project was created with
```bash
npm init svelte@next svelte-timeline
cd svelte-timeline
npx svelte-add@latest tailwindcss
npm install -D svelte2tsx
```
