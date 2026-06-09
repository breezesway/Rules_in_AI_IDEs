---
to: app/components/<%= name %>/<%= name %>.nuxt.test.ts
---
// @vitest-environment nuxt
import { describe, it, expect, beforeEach } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import type { VueWrapper } from "@vue/test-utils";
import <%= name %> from './<%= name %>.vue'

describe('<%= name %>', () => {
  let wrapper: VueWrapper

  beforeEach(async () => {
    wrapper = await mountSuspended(<%= name %>, {
      props: {
        someProp: 'Test <%= name %>'
      }
    })
  })

  it('renders correctly', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('.<%= name.toLowerCase() %>-component').exists()).toBe(true)
  })

  // Add more tests here
  // make sure to handle edge cases
})
