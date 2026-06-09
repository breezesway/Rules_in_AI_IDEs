import { container } from "tsyringe";
import { DeepSeekService, DeepSeekServiceSingleton } from "./services/deepseek.service";
import type { IDeepSeekService } from "./services/deepseek.service";
import { PromptController, PromptControllerSingleton } from "./controllers/prompt.controller";
import type { IPromptController } from "./controllers/prompt.controller";

// Register the dependencies
container.register<IDeepSeekService>("IDeepSeekService", {
  useClass: DeepSeekServiceSingleton
});

container.register<IPromptController>("IPromptController", {
  useClass: PromptControllerSingleton
});

export { container }; 