<script setup lang="ts">
definePageMeta({
  title: "Accordion Demo",
  description: "A vertically stacked set of interactive headings",
});
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Accordion</h1>
      <p class="text-muted-foreground mt-2">
        A vertically stacked set of interactive headings that each reveal a
        section of content.
      </p>
    </div>

    <!-- Single Accordion -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Single Accordion</h2>
      <Accordion type="single" collapsible class="w-full">
        <AccordionItem value="item-1">
          <AccordionTrigger>Is it accessible?</AccordionTrigger>
          <AccordionContent>
            Yes. It adheres to the WAI-ARIA design pattern and is built with
            keyboard navigation in mind.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-2">
          <AccordionTrigger>Is it styled?</AccordionTrigger>
          <AccordionContent>
            Yes. It comes with default styles that match the other components'
            aesthetic.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-3">
          <AccordionTrigger>Is it animated?</AccordionTrigger>
          <AccordionContent>
            Yes. It's animated by default, but you can disable it if you prefer.
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>

    <!-- Multiple Accordion -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Multiple Accordion</h2>
      <Accordion type="multiple" class="w-full">
        <AccordionItem value="item-1">
          <AccordionTrigger>Framework Support</AccordionTrigger>
          <AccordionContent>
            This component library works with Vue.js, Nuxt.js, and other
            Vue-based frameworks.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-2">
          <AccordionTrigger>Customization</AccordionTrigger>
          <AccordionContent>
            You can customize the appearance using Tailwind CSS classes or by
            modifying the component styles.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="item-3">
          <AccordionTrigger>TypeScript Support</AccordionTrigger>
          <AccordionContent>
            Full TypeScript support is included out of the box for better
            development experience.
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>

    <!-- FAQ Example -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">FAQ Example</h2>
      <Accordion type="single" collapsible class="w-full">
        <AccordionItem value="faq-1">
          <AccordionTrigger
            >What payment methods do you accept?</AccordionTrigger
          >
          <AccordionContent>
            We accept all major credit cards, PayPal, Apple Pay, and Google Pay.
            All payments are processed securely through our payment provider.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="faq-2">
          <AccordionTrigger>How long does shipping take?</AccordionTrigger>
          <AccordionContent>
            Standard shipping takes 3-5 business days. Express shipping is
            available for 1-2 business days. International shipping varies by
            location.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="faq-3">
          <AccordionTrigger>Can I return my purchase?</AccordionTrigger>
          <AccordionContent>
            Yes, we offer a 30-day return policy for most items. Items must be
            in original condition and packaging. Some restrictions apply for
            personalized items.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="faq-4">
          <AccordionTrigger>Do you offer customer support?</AccordionTrigger>
          <AccordionContent>
            We provide 24/7 customer support via email and live chat. Our
            support team typically responds within 2-4 hours during business
            days.
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  </div>
</template>
