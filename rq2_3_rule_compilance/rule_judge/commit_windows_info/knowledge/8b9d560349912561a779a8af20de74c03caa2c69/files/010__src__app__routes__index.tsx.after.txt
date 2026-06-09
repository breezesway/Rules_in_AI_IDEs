import { createFileRoute } from '@tanstack/react-router';

import { TypographyH4 } from '@/shared/components/shadcn-ui/typography';

export const Route = createFileRoute('/')({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <div>
      <TypographyH4>Home</TypographyH4>
    </div>
  );
}
