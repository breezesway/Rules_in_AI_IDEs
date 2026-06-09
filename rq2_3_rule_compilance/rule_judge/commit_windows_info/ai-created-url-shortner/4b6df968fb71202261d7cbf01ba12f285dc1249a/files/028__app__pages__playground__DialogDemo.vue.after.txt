<script setup lang="ts">
definePageMeta({
  title: "Dialog Demo",
  description: "Modal dialog windows and overlays",
});

const isConfirmOpen = ref(false);
const isFormOpen = ref(false);
const userName = ref("");
const userEmail = ref("");

const handleSave = () => {
  // Handle form submission
  isFormOpen.value = false;
  userName.value = "";
  userEmail.value = "";
};

const handleConfirm = () => {
  isConfirmOpen.value = false;
};
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Dialog</h1>
      <p class="text-muted-foreground mt-2">
        A window overlaid on either the primary window or another dialog window.
      </p>
    </div>

    <!-- Basic Dialog -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Basic Dialog</h2>
      <Dialog>
        <DialogTrigger as-child>
          <Button>Open Dialog</Button>
        </DialogTrigger>
        <DialogContent class="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Edit profile</DialogTitle>
            <DialogDescription>
              Make changes to your profile here. Click save when you're done.
            </DialogDescription>
          </DialogHeader>
          <div class="grid gap-4 py-4">
            <div class="grid grid-cols-4 items-center gap-4">
              <Label for="name" class="text-right">Name</Label>
              <Input id="name" value="Pedro Duarte" class="col-span-3" />
            </div>
            <div class="grid grid-cols-4 items-center gap-4">
              <Label for="username" class="text-right">Username</Label>
              <Input id="username" value="@peduarte" class="col-span-3" />
            </div>
          </div>
          <DialogFooter>
            <Button type="submit">Save changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>

    <!-- Confirmation Dialog -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Confirmation Dialog</h2>
      <div class="flex gap-4">
        <Dialog v-model:open="isConfirmOpen">
          <DialogTrigger as-child>
            <Button variant="destructive">Delete Account</Button>
          </DialogTrigger>
          <DialogContent class="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>Are you absolutely sure?</DialogTitle>
              <DialogDescription>
                This action cannot be undone. This will permanently delete your
                account and remove your data from our servers.
              </DialogDescription>
            </DialogHeader>
            <DialogFooter class="sm:justify-start">
              <DialogClose as-child>
                <Button type="button" variant="secondary"> Cancel </Button>
              </DialogClose>
              <Button
                type="button"
                variant="destructive"
                @click="handleConfirm"
              >
                Delete Account
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </div>

    <!-- Form Dialog -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Form Dialog</h2>
      <Dialog v-model:open="isFormOpen">
        <DialogTrigger as-child>
          <Button>Create User</Button>
        </DialogTrigger>
        <DialogContent class="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Create User</DialogTitle>
            <DialogDescription>
              Add a new user to your team. Fill in the details below.
            </DialogDescription>
          </DialogHeader>
          <form class="space-y-4" @submit.prevent="handleSave">
            <div class="space-y-2">
              <Label for="newName">Full Name</Label>
              <Input
                id="newName"
                v-model="userName"
                placeholder="Enter full name"
                required
              />
            </div>
            <div class="space-y-2">
              <Label for="newEmail">Email</Label>
              <Input
                id="newEmail"
                v-model="userEmail"
                type="email"
                placeholder="user@example.com"
                required
              />
            </div>
            <div class="space-y-2">
              <Label for="role">Role</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select a role" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="admin">Admin</SelectItem>
                  <SelectItem value="editor">Editor</SelectItem>
                  <SelectItem value="viewer">Viewer</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <DialogFooter>
              <DialogClose as-child>
                <Button type="button" variant="outline">Cancel</Button>
              </DialogClose>
              <Button type="submit">Create User</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>

    <!-- Info Dialog -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Info Dialog</h2>
      <Dialog>
        <DialogTrigger as-child>
          <Button variant="outline">View Details</Button>
        </DialogTrigger>
        <DialogContent class="sm:max-w-[600px]">
          <DialogHeader>
            <DialogTitle>Product Information</DialogTitle>
            <DialogDescription>
              Detailed information about this product
            </DialogDescription>
          </DialogHeader>
          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <h4 class="font-semibold">Product Name</h4>
                <p class="text-sm text-muted-foreground">Premium Widget</p>
              </div>
              <div>
                <h4 class="font-semibold">SKU</h4>
                <p class="text-sm text-muted-foreground">PW-001</p>
              </div>
              <div>
                <h4 class="font-semibold">Price</h4>
                <p class="text-sm text-muted-foreground">$99.99</p>
              </div>
              <div>
                <h4 class="font-semibold">Stock</h4>
                <p class="text-sm text-muted-foreground">42 units</p>
              </div>
            </div>
            <div>
              <h4 class="font-semibold">Description</h4>
              <p class="text-sm text-muted-foreground">
                This is a premium widget with advanced features and excellent
                build quality. Perfect for both personal and professional use.
              </p>
            </div>
            <div>
              <h4 class="font-semibold">Features</h4>
              <ul
                class="text-sm text-muted-foreground list-disc list-inside space-y-1"
              >
                <li>High-quality materials</li>
                <li>Advanced functionality</li>
                <li>Easy to use</li>
                <li>2-year warranty</li>
              </ul>
            </div>
          </div>
          <DialogFooter>
            <DialogClose as-child>
              <Button variant="outline">Close</Button>
            </DialogClose>
            <Button>Add to Cart</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>

    <!-- Scrollable Dialog -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Scrollable Dialog</h2>
      <Dialog>
        <DialogTrigger as-child>
          <Button variant="outline">Terms & Conditions</Button>
        </DialogTrigger>
        <DialogContent class="sm:max-w-[600px]">
          <DialogHeader>
            <DialogTitle>Terms and Conditions</DialogTitle>
            <DialogDescription>
              Please read our terms and conditions carefully
            </DialogDescription>
          </DialogHeader>
          <DialogScrollContent class="max-h-[300px] space-y-4">
            <div>
              <h4 class="font-semibold">1. Introduction</h4>
              <p class="text-sm text-muted-foreground">
                These terms and conditions outline the rules and regulations for
                the use of our service. By accessing this service, we assume you
                accept these terms and conditions.
              </p>
            </div>
            <div>
              <h4 class="font-semibold">2. Use License</h4>
              <p class="text-sm text-muted-foreground">
                Permission is granted to temporarily download one copy of the
                materials for personal, non-commercial transitory viewing only.
                This is the grant of a license, not a transfer of title.
              </p>
            </div>
            <div>
              <h4 class="font-semibold">3. Disclaimer</h4>
              <p class="text-sm text-muted-foreground">
                The materials on our service are provided on an 'as is' basis.
                We make no warranties, expressed or implied, and hereby disclaim
                and negate all other warranties.
              </p>
            </div>
            <div>
              <h4 class="font-semibold">4. Limitations</h4>
              <p class="text-sm text-muted-foreground">
                In no event shall our company or its suppliers be liable for any
                damages arising out of the use or inability to use the materials
                on our service.
              </p>
            </div>
            <div>
              <h4 class="font-semibold">5. Privacy Policy</h4>
              <p class="text-sm text-muted-foreground">
                Your privacy is important to us. Our Privacy Policy explains how
                we collect, use, and protect your information when you use our
                service.
              </p>
            </div>
          </DialogScrollContent>
          <DialogFooter>
            <DialogClose as-child>
              <Button variant="outline">Decline</Button>
            </DialogClose>
            <DialogClose as-child>
              <Button>Accept</Button>
            </DialogClose>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  </div>
</template>
