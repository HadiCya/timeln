<script>
  import { Timeline, TimelineItem } from "flowbite-svelte";
  let events = [
    {
      date: "June 4, 1776",
      title: "Declaration of Independence",
      content:
        "The United States Declaration of Independence is adopted by the Continental Congress",
    },
    {
      date: "March 12, 1861",
      title: "American Civil War",
      content: "The American Civil War begins",
    },
    {
      date: "June 20, 1969",
      title: "Apollo 11",
      content:
        'Neil Armstrong and Edwin "Buzz" Aldrin become the first humans to walk on the Moon',
    },
    {
      date: "June 4, 1776",
      title: "Declaration of Independence",
      content:
        "The United States Declaration of Independence is adopted by the Continental Congress",
    },
    {
      date: "March 12, 1861",
      title: "American Civil War",
      content: "The American Civil War begins",
    },
    {
      date: "June 20, 1969",
      title: "Apollo 11",
      content:
        'Neil Armstrong and Edwin "Buzz" Aldrin become the first humans to walk on the Moon',
    },
    {
      date: "June 4, 1776",
      title: "Declaration of Independence",
      content:
        "The United States Declaration of Independence is adopted by the Continental Congress",
    },
    {
      date: "March 12, 1861",
      title: "American Civil War",
      content: "The American Civil War begins",
    },
    {
      date: "June 20, 1969",
      title: "Apollo 11",
      content:
        'Neil Armstrong and Edwin "Buzz" Aldrin become the first humans to walk on the Moon',
    },
  ];

  function toggleContent(event) {
    event.show = !event.show;
    events = events;
  }
</script>

<Timeline order="horizontal" class="timeline">
  {#each events as event}
    <div class="tl-item">
      <TimelineItem title={event.title} date={event.date}>
        <svelte:fragment slot="icon">
          <div class="flex items-center">
            <button
              class="flex z-10 justify-center items-center w-6 h-6 bg-primary-200 rounded-full ring-0 ring-white dark:bg-primary-900 sm:ring-8 dark:ring-gray-900 shrink-0"
              on:click={() => toggleContent(event)}
              aria-label="Toggle content"
            />
            <div
              class="hidden sm:flex w-full bg-gray-200 h-0.5 dark:bg-gray-700"
            />
          </div>
        </svelte:fragment>
        {#if event.show}
          <p class="text-base font-normal text-gray-500 dark:text-gray-400">
            {event.content}
          </p>
        {/if}
      </TimelineItem>
    </div>
  {/each}
</Timeline>
