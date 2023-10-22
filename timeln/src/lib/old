<script>
  import { Timeline, TimelineItem } from "flowbite-svelte";
  import PopupBox from "./PopupBox.svelte";
  let events = [
    {
      date: "June 4, 1776",
      title: "Declaration of Independence",
      content:
        "The United States Declaration of Independence is adopted by the Continental Congress",
      textOpacity: 0,
    },
    {
      date: "March 12, 1861",
      title: "American Civil War",
      content: "The American Civil War begins",
      textOpacity: 0,
    },
    {
      date: "June 20, 1969",
      title: "Apollo 11",
      content:
        'Neil Armstrong and Edwin "Buzz" Aldrin become the first humans to walk on the Moon',
      textOpacity: 0,
    },
    {
      date: "June 4, 1776",
      title: "Declaration of Independence",
      content:
        "The United States Declaration of Independence is adopted by the Continental Congress",
      textOpacity: 0,
    },
    {
      date: "March 12, 1861",
      title: "American Civil War",
      content: "The American Civil War begins",
      textOpacity: 0,
    },
    {
      date: "June 20, 1969",
      title: "Apollo 11",
      content:
        'Neil Armstrong and Edwin "Buzz" Aldrin become the first humans to walk on the Moon',
      textOpacity: 0,
    },
  ];

  function toggleContent(event) {
    events.forEach((e) => {
      if (e !== event) {
        e.show = false;
        e.width = "150px";
        e.textOpacity = 0;
      }
    });

    event.show = !event.show;
    event.width = event.show ? event.title.length + 400 + "ch" : "150px";
    event.textOpacity = event.show ? 1 : 0;

    const buttonRect = event.buttonElement.getBoundingClientRect();
    event.buttonPosition = {
      top: buttonRect.top,
      left: buttonRect.left + event.title.length * 2,
    };

    events = events;
  }
</script>

<Timeline order="horizontal" class="timeline">
  {#each events as event}
    <div
      class="tl-item"
      style="width: {event.width}; transition: width 0.3s ease-in-out; "
    >
      <TimelineItem title={event.title} date={event.date}>
        <svelte:fragment slot="icon">
          <div class="flex items-center">
            <button
              class="flex z-10 justify-center items-center w-6 h-6 bg-primary-200 rounded-full ring-0 ring-white dark:bg-primary-900 sm:ring-8 dark:ring-gray-900 shrink-0"
              on:click={() => toggleContent(event)}
              aria-label="Toggle content"
              bind:this={event.buttonElement}
            />
            <div
              class="hidden sm:flex w-full bg-gray-200 h-0.5 dark:bg-gray-700"
            />
          </div>
        </svelte:fragment>
        {#if event.show}
          <PopupBox content={event.content} position={event.buttonPosition} />
        {/if}
      </TimelineItem>
    </div>
  {/each}
</Timeline>

<style>
  .tl-item {
    width: 200px;
    margin: 10px;
  }
</style>
