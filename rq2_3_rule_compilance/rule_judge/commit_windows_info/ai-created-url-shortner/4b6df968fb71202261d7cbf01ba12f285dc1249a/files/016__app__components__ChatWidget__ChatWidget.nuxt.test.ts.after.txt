// @vitest-environment nuxt
import { describe, it, expect, beforeEach } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import type { VueWrapper } from "@vue/test-utils";
import ChatWidget from './ChatWidget.vue'

describe('ChatWidget', () => {
  let wrapper: VueWrapper

  beforeEach(async () => {
    wrapper = await mountSuspended(ChatWidget, {
      props: {
        someProp: 'Test ChatWidget'
      }
    })
  })

  it('renders correctly', () => {
    expect(wrapper.exists()).toBe(true)
    expect(wrapper.find('.chatwidget-component').exists()).toBe(true)
  })

  // Add more tests here
  // make sure to handle edge cases
})
