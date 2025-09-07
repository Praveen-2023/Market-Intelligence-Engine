"""
Image Generation Service for upGrad AI Marketing Automation
Integrates with Stable Diffusion API for branded campaign visuals
"""

import os
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import base64
import json
import asyncio
import aiohttp
from PIL import Image, ImageDraw, ImageFont
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageGenerator:
    """
    AI-powered image generation for marketing campaigns
    Uses Stable Diffusion API for branded visuals
    """
    
    def __init__(self):
        self.stability_api_key = os.getenv('STABILITY_API_KEY')
        self.base_url = "https://api.stability.ai/v2beta/stable-image/generate"
        self.brand_guidelines = self._load_brand_guidelines()
        self.output_dir = Path("main idea/MI/images")
        self.output_dir.mkdir(exist_ok=True)
        
    def _load_brand_guidelines(self) -> Dict[str, Any]:
        """Load upGrad brand guidelines for image generation"""
        return {
            "colors": {
                "primary": "#007BFF",
                "secondary": "#FFFFFF", 
                "accent": "#FF6B35",
                "success": "#28A745",
                "warning": "#FFC107"
            },
            "fonts": ["Inter", "Arial", "Helvetica"],
            "logo_requirements": {
                "position": "top-right or bottom-right",
                "size": "prominent but not overwhelming",
                "background": "ensure good contrast"
            },
            "style_guidelines": {
                "mood": "professional, motivational, aspirational",
                "setting": "modern office, Indian professionals",
                "quality": "high resolution, marketing ready",
                "avoid": "cluttered, unprofessional, low quality"
            }
        }
    
    async def generate_campaign_image(self, 
                                    content_context: Dict[str, Any],
                                    image_type: str = "social_media") -> Optional[str]:
        """Generate branded campaign image using AI"""
        
        try:
            # Create optimized prompt
            prompt = self._create_image_prompt(content_context, image_type)
            
            # Generate image using Stable Diffusion
            if self.stability_api_key:
                image_path = await self._generate_with_stability_ai(prompt, image_type)
            else:
                # Fallback to creating a branded template
                image_path = self._create_branded_template(content_context, image_type)
            
            # Add branding overlay
            if image_path:
                branded_path = self._add_branding_overlay(image_path, content_context)
                return branded_path
            
            return None
            
        except Exception as e:
            logger.error(f"Error generating campaign image: {e}")
            # Return fallback template
            return self._create_branded_template(content_context, image_type)
    
    def _create_image_prompt(self, 
                           content_context: Dict[str, Any], 
                           image_type: str) -> str:
        """Create optimized prompt for image generation"""
        
        course = content_context.get('course', 'Professional Development')
        city = content_context.get('city', 'India')
        theme = content_context.get('theme', 'Career Growth')
        
        # Base prompt components
        base_elements = [
            "Professional marketing poster for upGrad education platform",
            f"Theme: {theme} in {course}",
            f"Setting: Modern office environment in {city}, India",
            "People: Diverse Indian professionals, confident and successful looking",
            "Age group: 25-40 years, business attire",
            "Mood: Inspiring, professional, aspirational, motivational"
        ]
        
        # Style specifications
        style_elements = [
            f"Colors: Primary blue ({self.brand_guidelines['colors']['primary']}) and orange ({self.brand_guidelines['colors']['accent']}) accents",
            "Style: Clean, modern, high-quality, professional photography style",
            "Background: Subtle tech/data visualization elements, clean gradient",
            "Lighting: Professional, well-lit, corporate photography lighting"
        ]
        
        # Quality specifications
        quality_elements = [
            "Quality: High resolution, 4K, marketing-ready",
            "Composition: Rule of thirds, professional framing",
            "Text space: Leave space for text overlay in bottom third"
        ]
        
        # Image type specific adjustments
        if image_type == "social_media":
            quality_elements.append("Aspect ratio: Square (1:1) for social media")
        elif image_type == "email_header":
            quality_elements.append("Aspect ratio: Wide banner (16:9)")
        elif image_type == "display_ad":
            quality_elements.append("Aspect ratio: Standard display (4:3)")
        
        # Negative prompt elements
        negative_elements = [
            "Negative prompt: blurry, low quality, unprofessional, cluttered",
            "cartoon, anime, text errors, watermarks, signatures",
            "poor lighting, amateur photography, distorted faces"
        ]
        
        # Combine all elements
        full_prompt = " | ".join(base_elements + style_elements + quality_elements)
        negative_prompt = ", ".join([elem.replace("Negative prompt: ", "") for elem in negative_elements if "Negative prompt:" in elem])
        
        return {
            "prompt": full_prompt,
            "negative_prompt": negative_prompt
        }
    
    async def _generate_with_stability_ai(self, 
                                        prompt_data: Dict[str, str], 
                                        image_type: str) -> Optional[str]:
        """Generate image using Stability AI API"""
        
        if not self.stability_api_key:
            logger.warning("Stability AI API key not available")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.stability_api_key}",
                "Accept": "image/*"
            }
            
            # Determine image dimensions based on type
            dimensions = self._get_image_dimensions(image_type)
            
            payload = {
                "prompt": prompt_data["prompt"],
                "negative_prompt": prompt_data["negative_prompt"],
                "output_format": "png",
                "aspect_ratio": dimensions["aspect_ratio"],
                "seed": 42,  # For consistency
                "style_preset": "photographic"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/core",
                    headers=headers,
                    data=payload
                ) as response:
                    
                    if response.status == 200:
                        image_data = await response.read()
                        
                        # Save image
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"campaign_{image_type}_{timestamp}.png"
                        image_path = self.output_dir / filename
                        
                        with open(image_path, 'wb') as f:
                            f.write(image_data)
                        
                        logger.info(f"Generated image saved: {image_path}")
                        return str(image_path)
                    else:
                        error_text = await response.text()
                        logger.error(f"Stability AI API error: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error calling Stability AI API: {e}")
            return None
    
    def _get_image_dimensions(self, image_type: str) -> Dict[str, Any]:
        """Get appropriate dimensions for different image types"""
        
        dimensions_map = {
            "social_media": {
                "aspect_ratio": "1:1",
                "width": 1024,
                "height": 1024
            },
            "email_header": {
                "aspect_ratio": "16:9", 
                "width": 1920,
                "height": 1080
            },
            "display_ad": {
                "aspect_ratio": "4:3",
                "width": 1200,
                "height": 900
            },
            "story": {
                "aspect_ratio": "9:16",
                "width": 1080,
                "height": 1920
            }
        }
        
        return dimensions_map.get(image_type, dimensions_map["social_media"])
    
    def _create_branded_template(self, 
                               content_context: Dict[str, Any], 
                               image_type: str) -> str:
        """Create a branded template when AI generation is not available"""
        
        try:
            dimensions = self._get_image_dimensions(image_type)
            width, height = dimensions["width"], dimensions["height"]
            
            # Create base image with gradient background
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            
            # Create gradient background
            primary_color = self._hex_to_rgb(self.brand_guidelines['colors']['primary'])
            accent_color = self._hex_to_rgb(self.brand_guidelines['colors']['accent'])
            
            for y in range(height):
                # Create vertical gradient
                ratio = y / height
                r = int(primary_color[0] * (1 - ratio) + accent_color[0] * ratio)
                g = int(primary_color[1] * (1 - ratio) + accent_color[1] * ratio)
                b = int(primary_color[2] * (1 - ratio) + accent_color[2] * ratio)
                
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Add semi-transparent overlay for text readability
            overlay = Image.new('RGBA', (width, height), (255, 255, 255, 128))
            image = Image.alpha_composite(image.convert('RGBA'), overlay)
            
            # Add text content
            self._add_text_to_template(image, content_context, image_type)
            
            # Save template
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"template_{image_type}_{timestamp}.png"
            image_path = self.output_dir / filename
            
            image.convert('RGB').save(image_path, 'PNG', quality=95)
            
            logger.info(f"Created branded template: {image_path}")
            return str(image_path)
            
        except Exception as e:
            logger.error(f"Error creating branded template: {e}")
            return None
    
    def _add_text_to_template(self, 
                            image: Image.Image, 
                            content_context: Dict[str, Any], 
                            image_type: str):
        """Add text content to the template image"""
        
        draw = ImageDraw.Draw(image)
        width, height = image.size
        
        try:
            # Try to load a nice font
            title_font = ImageFont.truetype("arial.ttf", size=int(height * 0.08))
            subtitle_font = ImageFont.truetype("arial.ttf", size=int(height * 0.05))
            body_font = ImageFont.truetype("arial.ttf", size=int(height * 0.04))
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        
        # Add upGrad logo text
        logo_text = "upGrad"
        logo_bbox = draw.textbbox((0, 0), logo_text, font=title_font)
        logo_width = logo_bbox[2] - logo_bbox[0]
        logo_x = width - logo_width - 50
        logo_y = 50
        
        draw.text((logo_x, logo_y), logo_text, 
                 fill=self.brand_guidelines['colors']['primary'], font=title_font)
        
        # Add main content
        course = content_context.get('course', 'Professional Development')
        city = content_context.get('city', 'India')
        
        main_text = f"Transform Your Career with {course}"
        main_bbox = draw.textbbox((0, 0), main_text, font=subtitle_font)
        main_width = main_bbox[2] - main_bbox[0]
        main_x = (width - main_width) // 2
        main_y = height // 2 - 100
        
        draw.text((main_x, main_y), main_text, fill='white', font=subtitle_font)
        
        # Add location
        location_text = f"Opportunities in {city}"
        location_bbox = draw.textbbox((0, 0), location_text, font=body_font)
        location_width = location_bbox[2] - location_bbox[0]
        location_x = (width - location_width) // 2
        location_y = main_y + 80
        
        draw.text((location_x, location_y), location_text, fill='white', font=body_font)
        
        # Add call to action
        cta_text = "Enroll Now - Limited Seats!"
        cta_bbox = draw.textbbox((0, 0), cta_text, font=body_font)
        cta_width = cta_bbox[2] - cta_bbox[0]
        cta_x = (width - cta_width) // 2
        cta_y = height - 150
        
        # Add CTA background
        padding = 20
        cta_bg_coords = [
            cta_x - padding, cta_y - padding,
            cta_x + cta_width + padding, cta_y + 50
        ]
        draw.rectangle(cta_bg_coords, fill=self.brand_guidelines['colors']['accent'])
        
        draw.text((cta_x, cta_y), cta_text, fill='white', font=body_font)
    
    def _add_branding_overlay(self, 
                            image_path: str, 
                            content_context: Dict[str, Any]) -> str:
        """Add branding overlay to generated image"""
        
        try:
            # Open the generated image
            with Image.open(image_path) as img:
                # Create a copy to work with
                branded_img = img.copy()
                draw = ImageDraw.Draw(branded_img)
                
                width, height = branded_img.size
                
                # Add upGrad watermark
                try:
                    font = ImageFont.truetype("arial.ttf", size=max(24, int(height * 0.03)))
                except:
                    font = ImageFont.load_default()
                
                watermark_text = "upGrad"
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = bbox[2] - bbox[0]
                
                # Position in bottom right
                x = width - text_width - 30
                y = height - 60
                
                # Add semi-transparent background
                bg_coords = [x - 10, y - 10, x + text_width + 10, y + 40]
                draw.rectangle(bg_coords, fill=(0, 0, 0, 128))
                
                # Add text
                draw.text((x, y), watermark_text, 
                         fill=self.brand_guidelines['colors']['primary'], font=font)
                
                # Save branded version
                branded_path = image_path.replace('.png', '_branded.png')
                branded_img.save(branded_path, 'PNG', quality=95)
                
                logger.info(f"Added branding overlay: {branded_path}")
                return branded_path
                
        except Exception as e:
            logger.error(f"Error adding branding overlay: {e}")
            return image_path  # Return original if branding fails
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def get_image_variations(self, 
                           base_image_path: str, 
                           variations: List[str]) -> List[str]:
        """Generate variations of a base image"""
        
        variation_paths = []
        
        for variation in variations:
            try:
                # This would implement actual image variation logic
                # For now, return the base image with different names
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                variation_path = base_image_path.replace('.png', f'_{variation}_{timestamp}.png')
                
                # Copy the base image as variation (placeholder)
                with Image.open(base_image_path) as img:
                    img.save(variation_path)
                
                variation_paths.append(variation_path)
                
            except Exception as e:
                logger.error(f"Error creating variation {variation}: {e}")
        
        return variation_paths
    
    def optimize_for_platform(self, 
                            image_path: str, 
                            platform: str) -> str:
        """Optimize image for specific social media platform"""
        
        platform_specs = {
            "facebook": {"size": (1200, 630), "format": "JPEG"},
            "instagram": {"size": (1080, 1080), "format": "JPEG"},
            "linkedin": {"size": (1200, 627), "format": "PNG"},
            "twitter": {"size": (1200, 675), "format": "JPEG"},
            "youtube": {"size": (1280, 720), "format": "JPEG"}
        }
        
        spec = platform_specs.get(platform.lower())
        if not spec:
            return image_path
        
        try:
            with Image.open(image_path) as img:
                # Resize for platform
                optimized_img = img.resize(spec["size"], Image.Resampling.LANCZOS)
                
                # Save optimized version
                optimized_path = image_path.replace('.png', f'_{platform}.{spec["format"].lower()}')
                optimized_img.save(optimized_path, spec["format"], quality=90)
                
                logger.info(f"Optimized image for {platform}: {optimized_path}")
                return optimized_path
                
        except Exception as e:
            logger.error(f"Error optimizing for {platform}: {e}")
            return image_path

# Global instance
image_generator = ImageGenerator()
